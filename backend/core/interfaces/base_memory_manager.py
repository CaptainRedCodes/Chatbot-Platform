
import abc
from typing import Any, Dict


class BaseMemoryStrategy(abc.ABC):
    """Abstract base class for all memory strategies."""
    
    @abc.abstractmethod
    def add_message(self, user_input: str, ai_response: str) -> None:
        """
        Add a new user-AI interaction to the memory storage.
        """
        pass
    
    @abc.abstractmethod
    def get_context(self, query: str) -> str:
        """
        Retrieve and format relevant context from memory for the LLM.
        """
        pass
    
    @abc.abstractmethod
    def clear(self) -> None:
        """
        Reset the memory storage, useful for starting new conversations.
        """
        pass
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the current memory usage.
        """
        return {
            "strategy_type": self.__class__.__name__,
            "memory_size": "Unknown"
        }