
from abc import ABC, abstractmethod
from backend.core.openai_client import get_openai_client
from backend.core.messages import ErrorMessages


class BaseSummarizer(ABC):

    @abstractmethod
    async def summarize(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generate a summary given a prompt and optional system prompt.
        """
        pass


class OpenRouterSummarizer(BaseSummarizer):

    def __init__(self, model: str = "meta-llama/llama-3.3-70b-instruct:free"):
        self.model = model
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


def get_summarizer(model: str = "meta-llama/llama-3.3-70b-instruct:free") -> BaseSummarizer:
    """Get Summary"""
    return OpenRouterSummarizer(model=model)
