from typing import Optional
from openai import AsyncOpenAI


_openai_client: Optional[AsyncOpenAI] = None

def get_openai_client() -> AsyncOpenAI:
    """Get OpenRouter client configured for OpenRouter API"""
    from backend.core.config import settings
    
    global _openai_client
    
    if _openai_client is None:
        _openai_client = AsyncOpenAI(
            base_url=settings.OPENROUTER_URL,
            api_key=settings.OPENROUTER_API_KEY,
            default_headers={
                "HTTP-Referer": "http://localhost:5173",  # Required by OpenRouter
                "X-Title": "ChatBot Platform",           # App name for OpenRouter dashboard
            }
        )
    
    return _openai_client