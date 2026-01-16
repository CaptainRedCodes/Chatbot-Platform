from datetime import datetime
from threading import Lock
from typing import Optional, List, Dict
from uuid import uuid4

from backend.core import supabase_client
from backend.core.interfaces.base_llm_manager import BaseLLMManager
from backend.services.llm.provider import get_llm_provider

class SessionManager:
    """
    Manages multiple chatbot sessions.
    """
    
    def __init__(self):
        self.sessions: dict[str, BaseLLMManager] = {}
        self.db = supabase_client.get_supabase_client()
        self._lock = Lock()
    
    def create_session(
        self, 
        user_id: str,
        project_id: str,
        session_id: Optional[str] = None,
        chat_model: str = "gpt-4o-mini",
        summary_model: str = "gpt-3.5-turbo",
        enable_db: bool = True
    ) -> tuple[str, BaseLLMManager]:
        """
        Create a new chatbot session.
        """
        if session_id is None:
            session_id = str(uuid4())
        
        if session_id in self.sessions:
            return session_id, self.sessions[session_id]
        
        # Create ChatBot instance
        chatbot = get_llm_provider(
            session_id=session_id,
            project_id=project_id,
            user_id=user_id,
            chat_model=chat_model,
            summary_model=summary_model,
            enable_db=enable_db
        )
        
        # Persist session metadata
        if enable_db and self.db:
            try:
                data = {
                    "id": session_id,
                    "user_id": user_id,
                    "project_id": project_id,
                    "created_at": datetime.utcnow().isoformat(),
                    "title": "New Chat"
                }
                self.db.table("sessions").insert(data).execute()
            except Exception as e:
                print(f"Error creating session in DB: {e}")

        with self._lock:
            self.sessions[session_id] = chatbot
            
        return session_id, chatbot
    
    def get_session(self, session_id: str) -> Optional[BaseLLMManager]:
        """Get existing session, loading from DB if needed."""
        if session_id in self.sessions:
            return self.sessions[session_id]
            
        # Try to load from DB
        if self.db:
            try:
                res = self.db.table("sessions").select("*").eq("id", session_id).execute()
                if res.data:
                    project_id = res.data[0].get("project_id", "")
                    user_id = res.data[0].get("user_id", "")
                    chat_model = res.data[0].get("model", "gpt-4o-mini")
                    summary_model = res.data[0].get("model","gpt-3.5-turbo")
                    enable_db = res.data[0].get("enable_db", True)

                    chatbot = get_llm_provider(
                                session_id=session_id,
                                project_id=project_id,
                                user_id=user_id,
                                chat_model=chat_model,
                                summary_model=summary_model,
                                enable_db=enable_db
                            )
                    
                    with self._lock:
                        self.sessions[session_id] = chatbot
                    return chatbot
            except Exception as e:
                print(f"Error loading session: {e}")
                
        return None
    
    def end_session(self, session_id: str) -> bool:
        """End and cleanup session."""
        if session_id in self.sessions:
            self.sessions[session_id].reset_conversation()
            with self._lock:
                del self.sessions[session_id]
        
        # Always try to delete from DB to keep robust
        if self.db:
            try:
                self.db.table("sessions").delete().eq("id", session_id).execute()
                self.db.table("messages").delete().eq("session_id", session_id).execute()
                return True
            except Exception as e:
                print(f"Error checking db deletion: {e}")
                
        return False

    def get_user_sessions(self, user_id: str, project_id: Optional[str] = None) -> List[Dict]:
        """List sessions for a user/project."""
        if not self.db:
            return []
            
        query = self.db.table("sessions").select("*").eq("user_id", user_id)
        if project_id:
            query = query.eq("project_id", project_id)
            
        res = query.order("created_at", desc=True).execute()
        return res.data if res.data else []

    
    def get_active_sessions(self) -> list[str]:
        """Get list of active session IDs."""
        return list(self.sessions.keys())
    
    def get_session_count(self) -> int:
        """Get number of active sessions."""
        return len(self.sessions)