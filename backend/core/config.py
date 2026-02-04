from typing import ClassVar, List
from pydantic_settings import BaseSettings, SettingsConfigDict


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
        'meta-llama/llama-3.3-70b-instruct:free',   # Llama 3.3 70B -
        'google/gemma-3-27b-it:free',                # Google Gemma 3 27B 
        'google/gemini-2.0-flash-exp:free',          # Gemini 2.0 Flash
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )


settings = Settings()
