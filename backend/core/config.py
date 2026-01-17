import logging
from typing import ClassVar, List
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)
class Settings(BaseSettings):
    """Application settings"""

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_URL:str = ""
    FREE_MODELS: ClassVar[List[str]] = [
        'meta-llama/llama-3.3-70b-instruct:free', 
        'deepseek/deepseek-r1-0528:free', 
        'qwen/qwen3-coder:free'
    ]
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

settings = Settings()
