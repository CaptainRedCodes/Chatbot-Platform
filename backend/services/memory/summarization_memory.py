import asyncio
from typing import Dict, List
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
from backend.services.llm.summarizer import get_summarizer
from backend.core.supabase_client import get_supabase_client
from backend.core.interfaces.base_memory_manager import BaseMemoryStrategy
from backend.core.messages import ErrorMessages
from backend.core.config import DEFAULT_MODEL



class SummarizationMemory(BaseMemoryStrategy):
    
    def __init__(
        self, 
        session_id: str,
        project_id: str,
        user_id: str,
        summary_threshold: int = 12,
        model_name: str = DEFAULT_MODEL,
        enable_db_persistence: bool = True
    ):
        
        super().__init__()
        self.session_id = session_id
        self.project_id = project_id
        self.user_id = user_id
        self.summary_threshold = summary_threshold
        self.model_name = model_name
        self.enable_db_persistence = enable_db_persistence
        
        # Use lightweight summarizer to avoid circular dependency
        self.summarizer = get_summarizer(model=self.model_name)
        
        if self.enable_db_persistence:
            self.db = get_supabase_client()
        else:
            self.db = None
        
        self.running_summary = ""
        self.buffer: List[Dict[str, str]] = []
        self._summarization_in_progress = False
        
        self.executor = ThreadPoolExecutor(max_workers=2)

        if self.enable_db_persistence and self.db:
            self.load_memory()

    def load_memory(self):
        try:
            summary_response = self.db.table("messages")\
                .select("content")\
                .eq("session_id", self.session_id)\
                .eq("role", "system")\
                .ilike("content", "[SUMMARY]%")\
                .order("timestamp", desc=True)\
                .limit(1)\
                .execute()
            
            if summary_response.data:
                self.running_summary = summary_response.data[0]['content'].replace("[SUMMARY] ", "")

            msgs_response = self.db.table("messages")\
                .select("role, content")\
                .eq("session_id", self.session_id)\
                .in_("role", ["user", "assistant"])\
                .order("timestamp", desc=True)\
                .limit(10)\
                .execute()
            
            if msgs_response.data:
                for msg in reversed(msgs_response.data):
                    self.buffer.append({"role": msg['role'], "content": msg['content']})
                    
        except Exception as e:
            print(f"{ErrorMessages.MEMORY_LOAD_FAILED}: {e}")

    def _save_to_db_async(self, role: str, content: str) -> None:
        if not self.enable_db_persistence or not self.db:
            return
        
        def _save():
            try:
                data = {
                    "session_id": self.session_id,
                    "role": role,
                    "content": content,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                self.db.table("messages").insert(data).execute() # type: ignore
            except Exception as e:
                print(f"{ErrorMessages.MEMORY_SAVE_FAILED}: {e}")
        
        self.executor.submit(_save)
    
    async def add_message(self, user_input: str, ai_response: str):
        self.buffer.append({"role": "user", "content": user_input})
        self.buffer.append({"role": "assistant", "content": ai_response})
        
        self._save_to_db_async("user", user_input)
        self._save_to_db_async("assistant", ai_response)
        
        # Fire-and-forget background summarization for lower latency
        if len(self.buffer) >= self.summary_threshold and not self._summarization_in_progress:
            asyncio.create_task(self._consolidate_memory_background())
    

    async def _consolidate_memory(self) -> None:
        if not self.buffer:
            return
        
        buffer_text = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in self.buffer
        ])
        
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
            response = await self.summarizer.summarize(
                prompt=user_prompt,
                system_prompt=system_prompt
            )
            
            self.running_summary = response.strip()
            
            if self.enable_db_persistence:
                self._save_to_db_async("system", f"[SUMMARY] {self.running_summary}")
            
        except Exception as e:
            print(f"{ErrorMessages.MEMORY_SUMMARIZE_FAILED}: {e}")
            return
        
        self.buffer = []

    async def _consolidate_memory_background(self) -> None:
        """Fire-and-forget background summarization for lower latency."""
        if self._summarization_in_progress:
            return
        
        self._summarization_in_progress = True
        try:
            await self._consolidate_memory()
        finally:
            self._summarization_in_progress = False
    
    def get_context(self) -> str:
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
        self.running_summary = ""
        self.buffer = []
    
    async def force_summarize(self) -> None:
        if self.buffer:
            await self._consolidate_memory()
    
    def __del__(self):
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)