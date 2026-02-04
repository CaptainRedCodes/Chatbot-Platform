from backend.core.interfaces.base_llm_manager import BaseLLMManager
from backend.core.config import settings, DEFAULT_MODEL
from backend.services.llm.openai_service import OpenAIProvider


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
    """
    
    # Ensure we never send an empty model to the provider
    if not chat_model or chat_model.strip() == "":
        chat_model = DEFAULT_MODEL
    
    if not summary_model or summary_model.strip() == "":
        summary_model = DEFAULT_MODEL
    
    provider = OpenAIProvider
    if not provider:
         raise ValueError(f"Unknown model: {chat_model}. Available models: {settings.FREE_MODELS}")
    
    return provider(
            session_id=session_id,
            project_id=project_id,
            user_id=user_id,
            summary_model=summary_model,
            chat_model=chat_model,
            enable_db=enable_db
        )  