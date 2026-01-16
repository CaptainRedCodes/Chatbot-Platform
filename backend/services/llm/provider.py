from backend.core.interfaces.base_llm_manager import BaseLLMManager
from backend.services.llm.openai_service import OpenAIProvider


def get_llm_provider(
    chat_model: str, 
    session_id: str, 
    project_id: str, 
    user_id: str,
    summary_model: str,
    enable_db: bool
) -> BaseLLMManager:
    """
    Factory: Decides which AI Provider class to use based on the model name.
    """
    
    if chat_model in ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]:
        return OpenAIProvider(
            session_id=session_id,
            project_id=project_id,
            user_id=user_id,
            chat_model=chat_model,
            summary_model=summary_model,
            enable_db=enable_db
        )
    
    # Default fallback
    return OpenAIProvider(session_id, project_id, user_id, chat_model, summary_model, enable_db)