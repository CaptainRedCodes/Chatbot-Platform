


from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator
from backend.core.config import DEFAULT_MODEL

# Constants for validation
MAX_MESSAGE_LENGTH = 10000
MAX_TITLE_LENGTH = 100

class Role(str,Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    role: Role
    content: str = Field(..., min_length=1, max_length=MAX_MESSAGE_LENGTH)
    
class ChatMessageStore(ChatMessage):
    id: Optional[str] = None
    session_id: str
    timestamp: datetime
    
class ChatSession(BaseModel):
    id: str
    project_id: str
    title: Optional[str] = Field(default="New Chat", max_length=MAX_TITLE_LENGTH)
    messages: List[ChatMessage] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

class SessionCreate(BaseModel):
    project_id: str
    title: Optional[str] = Field(default="New Chat", max_length=MAX_TITLE_LENGTH)
    chat_model: str = DEFAULT_MODEL

class SessionUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=MAX_TITLE_LENGTH)

class SessionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    project_id: str
    title: str
    chat_model: Optional[str] = Field(default=None, alias="model")  # Map 'model' from DB to 'chat_model'
    created_at: datetime

class ChatRequest(BaseModel):
    session_id: str
    message: str = Field(..., min_length=1, max_length=MAX_MESSAGE_LENGTH, description="User message to send to the chatbot")
    system_prompt: Optional[str] = None
    
    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Message cannot be empty or contain only whitespace')
        return v
    
class ChatResponse(BaseModel):
    response: str