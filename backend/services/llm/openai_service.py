"""
Example usage of SummarizationMemory in a chatbot application
"""

from backend.services.memory.summarization_memory import SummarizationMemory
from backend.core.openai_client import get_openai_client
from backend.core.interfaces.base_llm_manager import BaseLLMManager
from uuid import uuid4


class OpenAIProvider(BaseLLMManager):
    """
    Chatbot with summarization-based memory management.
    Optimized for low latency with async DB operations.
    """
    
    def __init__(
        self, 
        session_id: str = "",
        project_id: str = "",
        user_id: str = "",
        chat_model: str = "gpt-4o-mini", 
        summary_model: str = "gpt-3.5-turbo", 
        enable_db: bool = True
        ):

        super().__init__(session_id or str(uuid4),project_id,user_id)

        self.chat_model = chat_model
        self.ai_client = get_openai_client()
        
        # Initialize memory strategy
        self.memory = SummarizationMemory(
            session_id=self.session_id,
            summary_threshold=6,
            model_name=summary_model,
            enable_db_persistence=enable_db
        )
    

    def get_provider_name(self) -> str:
        return f"OpenAI,{self.chat_model}"
    

    async def chat(self, message: str, system_prompt: str = "") -> None:
        """
        Main chat method with low latency for OpenAI
        """
        context = self.memory.get_context(message)
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if context and context != "No conversation history available.":
            messages.append({
                "role": "system", 
                "content": f"Context from previous conversation:\n{context}"
            })
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.ai_client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            
            if not ai_response:
                ai_response = ""
                raise ValueError("Error in AI response")

            self.memory.add_message(message, ai_response)

            return ai_response
            
        except Exception as e:
            pass
    
    
    def reset_conversation(self):
        return super().reset_conversation()
