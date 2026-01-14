import logging
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)
class Settings(BaseSettings):
    """Application settings"""

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_URL:str = ""
    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
