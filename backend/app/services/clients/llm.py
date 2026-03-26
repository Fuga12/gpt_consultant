from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal


@dataclass
class LLMMessage:
    role: Literal["user", "assistant"]
    content: str


class LLMClient(ABC):
    @abstractmethod
    async def complete(self, system_prompt: str, messages: list[LLMMessage]) -> str: ...
