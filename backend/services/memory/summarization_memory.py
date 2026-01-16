from typing import Dict, List, Optional
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

from backend.core import supabase_client
from backend.core.openai_client import get_openai_client
from backend.models.chat import ChatMessage, ChatMessageStore, Role
from backend.core.interfaces.base_memory_manager import BaseMemoryStrategy


class SummarizationMemory(BaseMemoryStrategy):
    """
    Memory strategy using conversation summarization to maintain context
    while keeping token usage low for better latency.
    """
    
    def __init__(
        self, 
        session_id: str,
        summary_threshold: int = 6,
        model_name: str = "gpt-3.5-turbo",
        enable_db_persistence: bool = True
    ):
        """
        Args:
            session_id: Unique identifier for this conversation session
            summary_threshold: Number of messages before triggering summarization
            model_name: Model to use for summarization (use faster model)
            enable_db_persistence: Whether to save messages to database
        """
        self.session_id = session_id
        self.summary_threshold = summary_threshold
        self.model_name = model_name
        self.enable_db_persistence = enable_db_persistence
        
        # Initialize clients
        self.ai_client = get_openai_client()
        if self.enable_db_persistence:
            self.db = supabase_client.get_supabase_client()
        else:
            self.db = None
        
        self.running_summary = ""
        self.buffer: List[Dict[str, str]] = []
        
        # Thread pool for non-blocking DB writes
        self.executor = ThreadPoolExecutor(max_workers=2)

        # Load existing memory if enabled
        if self.enable_db_persistence and self.db:
            self.load_memory()

    def load_memory(self) -> None:
        """Load summary and recent messages from DB."""
        try:
            # 1. Get latest summary
            summary_response = self.db.table("messages")\
                .select("content")\
                .eq("session_id", self.session_id)\
                .eq("role", "system")\
                .ilike("content", "[SUMMARY]%")\
                .order("timestamp", desc=True)\
                .limit(1)\
                .execute()
            
            if summary_response.data:
                # Extract summary text (remove [SUMMARY] prefix)
                self.running_summary = summary_response.data[0]['content'].replace("[SUMMARY] ", "")

            # 2. Get recent non-summary messages
            # In a real app we might want to ensure we don't load messages already summarized,
            # but for simplicity we'll load the last N messages to fill the buffer.
            # Ideally, we should add a 'summarized' flag to messages in DB.
            # Here we just load the last few to provide immediate context.
            msgs_response = self.db.table("messages")\
                .select("role, content")\
                .eq("session_id", self.session_id)\
                .in_("role", ["user", "assistant"])\
                .order("timestamp", desc=True)\
                .limit(10)\
                .execute()
            
            if msgs_response.data:
                # They come in desc order (newest first), so reverse for buffer
                for msg in reversed(msgs_response.data):
                    self.buffer.append({"role": msg['role'], "content": msg['content']})
                    
        except Exception as e:
            print(f"[Memory Load Error]: {e}")

    
    def _save_to_db_async(self, role: str, content: str) -> None:
        """Non-blocking database save to maintain low latency."""
        if not self.enable_db_persistence or not self.db:
            return
        
        def _save():
            try:
                data = {
                    "session_id": self.session_id,
                    "role": role,
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat()
                }
                self.db.table("messages").insert(data).execute()
            except Exception as e:
                print(f"[DB Save Error]: {e}")
        
        self.executor.submit(_save)
    
    def add_message(self, user_input: str, ai_response: str) -> None:
        """
        Add new user-AI interaction to buffer.
        Triggers summarization if threshold is reached.
        Saves to DB asynchronously for low latency.
        """
        # Add to buffer
        self.buffer.append({"role": "user", "content": user_input})
        self.buffer.append({"role": "assistant", "content": ai_response})
        
        # Save to database asynchronously (non-blocking)
        self._save_to_db_async("user", user_input)
        self._save_to_db_async("assistant", ai_response)
        
        # Check if summarization is needed
        if len(self.buffer) >= self.summary_threshold:
            self._consolidate_memory()
    
    def _consolidate_memory(self) -> None:
        """
        Summarize buffer contents and merge with existing summary.
        Uses streaming-friendly approach for better perceived latency.
        """
        if not self.buffer:
            return
        
        # Format buffer for summarization
        buffer_text = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in self.buffer
        ])
        
        # Build summarization prompt
        if self.running_summary:
            system_prompt = (
                "You are a conversation summarizer. Create a concise, factual summary "
                "that preserves key information: names, dates, decisions, preferences, and context. "
                "Merge the previous summary with new messages into one coherent summary."
            )
            user_prompt = (
                f"Previous Summary:\n{self.running_summary}\n\n"
                f"New Messages:\n{buffer_text}\n\n"
                f"Provide an updated summary that combines both:"
            )
        else:
            system_prompt = (
                "You are a conversation summarizer. Create a concise, factual summary "
                "that captures key information: names, dates, decisions, preferences, and context."
            )
            user_prompt = f"Conversation:\n{buffer_text}\n\nProvide a summary:"
        
        try:
            # Generate summary using LLM
            response = self.ai_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  
                max_tokens=500  
            )
            
            self.running_summary = response.choices[0].message.content.strip()
            
            # Save summary to DB if persistence enabled
            if self.enable_db_persistence:
                self._save_to_db_async("system", f"[SUMMARY] {self.running_summary}")
            
            print(f"[Summary Updated: {len(self.running_summary)} chars]")
            
        except Exception as e:
            return
        
        self.buffer = []
    
    def get_context(self, query: str) -> str:
        """
        Build context for LLM from summary + recent buffer.
        This provides both long-term and short-term memory.
        """
        parts = []
        
        if self.running_summary:
            parts.append(f"## Previous Conversation Summary:\n{self.running_summary}")
        
        if self.buffer:
            buffer_text = "\n".join([
                f"{msg['role'].capitalize()}: {msg['content']}" 
                for msg in self.buffer
            ])
            parts.append(f"## Recent Messages:\n{buffer_text}")
        
        if not parts:
            return "No conversation history available."
        
        return "\n\n".join(parts)
    
    def clear(self) -> None:
        """Reset both summary and buffer."""
        self.running_summary = ""
        self.buffer = []
        print(f"[Memory cleared for session: {self.session_id}]")
    
    def force_summarize(self) -> None:
        """Manually trigger summarization regardless of threshold."""
        if self.buffer:
            self._consolidate_memory()
    
    def __del__(self):
        """Cleanup thread pool on deletion."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)