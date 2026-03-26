from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum
from typing import Literal


class PlatformType(StrEnum):
    TELEGRAM = "telegram"
    AVITO = "avito"
    WHATSAPP = "whatsapp"
    WEB = "web"


@dataclass
class Message:
    role: Literal["user", "assistant"]
    content: str


class Platform(ABC):
    platform_type: PlatformType

    @abstractmethod
    async def fetch_history(self, chat_id: str, credentials: dict) -> list[Message]: ...

    @abstractmethod
    async def send_message(self, chat_id: str, text: str, credentials: dict) -> None: ...


class PlatformFactory:
    _registry: dict[PlatformType, Platform] = {}

    @classmethod
    def register(cls, platform: Platform) -> None:
        cls._registry[platform.platform_type] = platform

    @classmethod
    def get(cls, platform_type: PlatformType) -> Platform:
        platform = cls._registry.get(platform_type)
        if platform is None:
            raise ValueError(f"Platform {platform_type!r} is not registered")
        return platform
