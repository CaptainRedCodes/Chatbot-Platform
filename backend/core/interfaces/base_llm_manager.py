from abc import ABC,abstractmethod

class BaseLLMManager(ABC):

    def __init__(self,session_id:str,project_id:str,user_id:str) -> None:
        self.session_id = session_id
        self.project_id = project_id,
        self.user_id = user_id
        self.memory = None


    @abstractmethod
    def get_provider_name(self) -> str:
        pass
    
    @abstractmethod
    async def chat(self,message:str,system_prompt:str = "")->str:
        pass

    @abstractmethod
    def reset_conversation(self):
        if self.memory:
            self.memory.clear()