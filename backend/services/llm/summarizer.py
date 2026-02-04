from backend.core.interfaces.base_summarizer_memory import BaseSummarizer
from backend.core.openai_client import get_openai_client
from backend.core.messages import ErrorMessages
from backend.core.config import DEFAULT_MODEL


class OpenRouterSummarizer(BaseSummarizer):
    """Summarizer using OpenRouter API."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model if model else DEFAULT_MODEL  # Ensure we never have empty model
        self.client = get_openai_client()
    
    async def summarize(self, prompt: str, system_prompt: str = "") -> str:
        """Generate summary using OpenRouter."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.5,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            return result.strip() if result else ""
            
        except Exception as e:
            print(f"{ErrorMessages.LLM_RESPONSE_FAILED}: {e}")
            return ""


def get_summarizer(model: str = DEFAULT_MODEL) -> BaseSummarizer:
    """Get summarizer instance."""
    return OpenRouterSummarizer(model=model)
