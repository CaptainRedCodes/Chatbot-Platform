
from abc import ABC, abstractmethod

class BaseSummarizer(ABC):

    @abstractmethod
    async def summarize(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generate a summary given a prompt and optional system prompt.
        """
        pass
