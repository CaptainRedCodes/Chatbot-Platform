from abc import ABC,abstractmethod
from typing import AsyncGenerator

class BaseLLMManager(ABC):
    """Abstract base class for all LLM strategies."""
    
    def __init__(self,session_id:str,project_id:str,user_id:str) -> None:
        self.session_id = session_id
        self.user_id = user_id
        if isinstance(project_id, tuple):
            self.project_id = str(project_id[0])
        elif project_id is None:
            self.project_id = ""
        else:
            self.project_id = str(project_id)
            
        self.memory = None


    @abstractmethod
    def get_provider_name(self) -> str:
        pass
    
    @abstractmethod
    async def chat(self,message:str,system_prompt:str = "")->str:
        """ Normal Chat"""
        pass

    @abstractmethod
    async def chat_stream(self, message: str, system_prompt: str = "") -> AsyncGenerator[str, None]:
        """Stream chat response token by token."""
        yield ""

    @abstractmethod
    def reset_conversation(self):
        if self.memory:
            self.memory.clear()