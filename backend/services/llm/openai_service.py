from backend.services.memory.summarization_memory import SummarizationMemory
from backend.core.openai_client import get_openai_client
from backend.core.interfaces.base_llm_manager import BaseLLMManager
from backend.core.messages import ErrorMessages
from uuid import uuid4
from typing import Union, List, Dict, AsyncGenerator

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
        chat_model: str = "meta-llama/llama-3.3-70b-instruct:free", 
        summary_model:str="meta-llama/llama-3.3-70b-instruct:free",
        enable_db: bool = True
        ):

        super().__init__(session_id or str(uuid4()), project_id, user_id)

        self.chat_model = chat_model
        self.ai_client = get_openai_client()
        self.summary_model = summary_model
        # Initialize memory strategy
        self.memory = SummarizationMemory(
            session_id=self.session_id,
            project_id=project_id,
            user_id=user_id,
            summary_threshold=6,
            model_name=summary_model,
            enable_db_persistence=enable_db
        )
    

    def get_provider_name(self) -> str:
        return f"OpenAI ({self.chat_model})"
    

    async def chat(self, message: Union[str, List[str], List[Dict]], system_prompt: str = "") -> str:
        """
        Main chat method with low latency for OpenAI
        """
        
        user_input_str = ""
        
        if isinstance(message, str):
            user_input_str = message
        elif isinstance(message, list):
            if len(message) > 0 and isinstance(message[0], dict):
                user_input_str = message[-1].get("content", "") # type: ignore
            else:
                user_input_str = "\n".join(str(x) for x in message)

        context = self.memory.get_context()
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if context and context != "No conversation history available.":
            messages.append({
                "role": "system", 
                "content": f"Context from previous conversation:\n{context}"
            })
    
        messages.append({"role": "user", "content": user_input_str})
        
        try:
            response = await self.ai_client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            
            if not ai_response:
                ai_response = ""
                raise ValueError(ErrorMessages.LLM_EMPTY_RESPONSE)

            await self.memory.add_message(user_input_str, ai_response)

            return ai_response
            
        except Exception as e:
            return f"{ErrorMessages.LLM_RESPONSE_FAILED}: {e}"


    async def chat_stream(self, message: str, system_prompt: str = "") -> AsyncGenerator[str, None]:
        """
        Stream chat response token by token for real-time display.
        """
        context = self.memory.get_context()
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        if context and context != "No conversation history available.":
            messages.append({
                "role": "system", 
                "content": f"Context from previous conversation:\n{context}"
            })
        
        messages.append({"role": "user", "content": message})
        
        full_response = ""
        
        try:
            stream = await self.ai_client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.5,
                max_tokens=1000,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full_response += token
                    yield token
            
            if full_response:
                await self.memory.add_message(message, full_response)
                
        except Exception as e:
            yield f"{ErrorMessages.LLM_RESPONSE_FAILED}: {e}"
    

    def reset_conversation(self):
        return super().reset_conversation()