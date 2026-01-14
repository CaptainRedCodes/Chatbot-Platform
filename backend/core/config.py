import logging
from pydantic_settings import BaseSettings
from backend.core.constants import Defaults, EnvVars

logger = logging.getLogger(__name__)
class Settings(BaseSettings):
    """Application settings"""

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    model_config = {"env_file": ".env", "case_sensitive": True}





settings = Settings()
