from datetime import datetime, timezone
from threading import Lock
from typing import Optional, List, Dict, Tuple
from uuid import uuid4
import logging

from backend.core import supabase_client
from backend.core.interfaces.base_llm_manager import BaseLLMManager
from backend.core.messages import ErrorMessages
from backend.services.llm.provider import get_llm_provider

logger = logging.getLogger(__name__)

class SessionManager:
    """
    Manages multiple chatbot sessions with optimized DB handling.
    """
    
    def __init__(self):
        self.sessions: Dict[str, BaseLLMManager] = {}
        self.db = supabase_client.get_supabase_client()
        self._lock = Lock()
    
    def create_session(
        self, 
        user_id: str,
        project_id: str,
        session_id: Optional[str] = None,
        chat_model: str = "meta-llama/llama-3.3-70b-instruct:free",
        summary_model: str = "meta-llama/llama-3.3-70b-instruct:free",
        enable_db: bool = True
    ) -> Tuple[str, BaseLLMManager]:
        """
        Create a new chatbot session and persist configuration.
        """
        if session_id is None:
            session_id = str(uuid4())
        
        # Check RAM cache first
        if session_id in self.sessions:
            return session_id, self.sessions[session_id]
        
        chatbot = get_llm_provider(
            session_id=session_id,
            project_id=project_id,
            user_id=user_id,
            chat_model=chat_model,
            summary_model=summary_model,
            enable_db=enable_db
        )
        
        if enable_db and self.db:
            try:
                data = {
                    "id": session_id,
                    "user_id": user_id,
                    "project_id": project_id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "title": "New Chat",
                    "model": chat_model 
                }
                self.db.table("sessions").insert(data).execute()
            except Exception as e:
                logger.error(f"{ErrorMessages.SESSION_CREATE_FAILED}: {e}")

        # Update Cache
        with self._lock:
            self.sessions[session_id] = chatbot
            
        return session_id, chatbot
    
    def get_session(self, session_id: str) -> Optional[BaseLLMManager]:
        """Get existing session, lazy-loading from DB if missing from RAM."""
        if session_id in self.sessions:
            return self.sessions[session_id]
            
        if not self.db:
            return None

        try:
            res = self.db.table("sessions")\
                .select("project_id, user_id, model")\
                .eq("id", session_id)\
                .single()\
                .execute()
            
            if res.data:
                project_id = res.data.get("project_id", "")
                user_id = res.data.get("user_id", "")
                chat_model = res.data.get("model", "meta-llama/llama-3.3-70b-instruct:free")
                
                # Reconstruct the bot
                chatbot = get_llm_provider(
                    session_id=session_id,
                    project_id=project_id,
                    user_id=user_id,
                    chat_model=chat_model,
                    summary_model=chat_model, 
                    enable_db=True
                )
                
                with self._lock:
                    self.sessions[session_id] = chatbot
                return chatbot
                
        except Exception as e:
            logger.error(f"{ErrorMessages.SESSION_LOAD_FAILED}: {e}")
                
        return None
    
    def get_user_sessions(self, user_id: str, project_id: Optional[str] = None) -> List[Dict]:
        """List sessions for a user, optimized for UI rendering."""
        if not self.db:
            return []
        
        try:
            query = self.db.table("sessions")\
                .select("id, title, created_at, model, project_id, user_id")\
                .eq("user_id", user_id)
            
            if project_id:
                query = query.eq("project_id", project_id)
                
            res = query.order("created_at", desc=True).execute()
            return res.data if res.data else []
            
        except Exception as e:
            logger.error(f"Failed to fetch sessions: {e}")
            return []

    def get_session_history(self, session_id: str) -> List[Dict]:
        """Get chat history optimized for frontend display."""
        if self.db:
            try:
                res = self.db.table("messages")\
                    .select("role, content, timestamp")\
                    .eq("session_id", session_id)\
                    .order("timestamp", desc=False)\
                    .execute()
                return res.data or []
            except Exception as e:
                logger.error(f"Failed to fetch history: {e}")
        return []

    def update_session(self, session_id: str, title: Optional[str] = None) -> Optional[Dict]:
        """Update session title."""
        if not self.db:
            return None
        
        try:
            update_data = {}
            if title is not None:
                update_data["title"] = title
            
            if not update_data:
                return None
            
            self.db.table("sessions")\
                .update(update_data)\
                .eq("id", session_id)\
                .execute()
            
            res = self.db.table("sessions").select("*").eq("id", session_id).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
            return None
            
        except Exception as e:
            logger.error(f"{ErrorMessages.SESSION_UPDATE_FAILED}: {e}")
            return None

    def end_session(self, session_id: str) -> bool:
        """End session and delete data."""

        if session_id in self.sessions:
            with self._lock:
                if session_id in self.sessions:
                    self.sessions[session_id].reset_conversation()
                    del self.sessions[session_id]
        
        if self.db:
            try:
                self.db.table("messages").delete().eq("session_id", session_id).execute()
                self.db.table("sessions").delete().eq("id", session_id).execute()
                return True
            except Exception as e:
                logger.error(f"{ErrorMessages.SESSION_DELETE_FAILED}: {e}")
                return False
        
        return True