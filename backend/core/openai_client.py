from openai import OpenAI

from backend.core.config import settings


def get_openai_client():
    client = OpenAI(
                base_url=settings.OPENROUTER_URL,
                api_key=settings.OPENROUTER_API_KEY)
    
    return client