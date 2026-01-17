from typing import List
from backend.core.interfaces.base_llm_manager import BaseLLMManager
from backend.core.config import settings


def get_llm_provider(
    chat_model: str, 
    session_id: str, 
    project_id: str, 
    user_id: str,
    summary_model: str,
    enable_db: bool = True
) -> BaseLLMManager:
    """
    Factory: Decides which AI Provider class to use based on the model name.
    All models are routed through OpenRouter (OpenAI-compatible API).
    """
    
    if chat_model in settings.FREE_MODELS:
        from backend.services.llm.openai_service import OpenAIProvider
        return OpenAIProvider(
            session_id=session_id,
            project_id=project_id,
            user_id=user_id,
            summary_model=summary_model,
            chat_model=chat_model,
            enable_db=enable_db
        )  
    else:
        raise ValueError(f"Unknown model: {chat_model}. Available models: {settings.FREE_MODELS}")