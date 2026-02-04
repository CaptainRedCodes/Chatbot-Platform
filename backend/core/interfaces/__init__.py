# Interfaces Module
# Export base classes for LLM and memory strategies

from backend.core.interfaces.base_llm_manager import BaseLLMManager
from backend.core.interfaces.base_memory_manager import BaseMemoryStrategy
from backend.core.interfaces.base_summarizer_memory import BaseSummarizer

__all__ = ["BaseLLMManager", "BaseMemoryStrategy", "BaseSummarizer"]
