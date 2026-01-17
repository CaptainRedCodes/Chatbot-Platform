from typing import Optional
from openai import AsyncOpenAI

from backend.core.config import settings

_openai_client: Optional[AsyncOpenAI] = None

def get_openai_client() -> AsyncOpenAI:
    global _openai_client
    
    if _openai_client is None:
        _openai_client = AsyncOpenAI(
            base_url=settings.OPENROUTER_URL,
            api_key=settings.OPENROUTER_API_KEY
        )
    
    return _openai_client