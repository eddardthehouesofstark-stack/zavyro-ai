from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AIProvider(ABC):
    @abstractmethod
    def complete(
        self,
        system_prompt: str,
        messages: List[Dict[str, str]],
        json_mode: bool = False,
        timeout_seconds: int = 15,
    ) -> str:
        """
        Executes a completion call against the AI model and returns response text.
        """
        pass
