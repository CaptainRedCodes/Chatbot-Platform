


from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class Role(str,Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    role: Role
    content: str
    
class ChatMessageStore(ChatMessage):
    id: Optional[str] = None
    session_id: str
    timestamp: datetime
    
class ChatSession(BaseModel):
    id: str
    project_id: str
    user_id: str
    title: Optional[str] = "New Chat"
    messages: List[ChatMessage] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

class SessionCreate(BaseModel):
    project_id: str
    user_id: Optional[str] = None
    title: Optional[str] = "New Chat"
    chat_model:str 

class SessionResponse(BaseModel):
    id: str
    project_id: str
    user_id: str
    title: str
    chat_model:str
    created_at: datetime

class ChatRequest(BaseModel):
    session_id:str
    message: str

class ChatResponse(BaseModel):
    response: str