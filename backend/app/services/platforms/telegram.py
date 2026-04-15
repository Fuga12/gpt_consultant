from __future__ import annotations

from app.clients.telegram import TelegramRegistry
from app.services.platforms.base import Message, Platform, PlatformType


class TelegramPlatform(Platform):
    platform_type = PlatformType.TELEGRAM

    def __init__(self, registry: TelegramRegistry) -> None:
        self._registry = registry

    async def fetch_history(self, chat_id: str, credentials: dict) -> list[Message]:
        return []

    async def send_message(self, chat_id: str, text: str, credentials: dict) -> None:
        client = self._registry.client_for_credentials(credentials)
        await client.send_message(chat_id, text)
