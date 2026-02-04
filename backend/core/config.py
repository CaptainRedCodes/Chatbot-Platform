import logging
from typing import ClassVar, List
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

# Default model - confirmed working on OpenRouter
DEFAULT_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

class Settings(BaseSettings):
    """Application settings"""

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_URL: str = "https://openrouter.ai/api/v1"
    
    # 3 Working free models on OpenRouter (2026)
    FREE_MODELS: ClassVar[List[str]] = [
        'meta-llama/llama-3.3-70b-instruct:free',   # Llama 3.3 70B - reliable, GPT-4 level
        'google/gemma-3-27b-it:free',                # Google Gemma 3 27B - multimodal, 128k context
        'google/gemini-2.0-flash-exp:free',          # Gemini 2.0 Flash - 1M context, multimodal
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )


settings = Settings()
