from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from app.services.bots.repository import BotRepository
from app.services.clients.llm import LLMClient
from app.services.platforms.base import PlatformType

if TYPE_CHECKING:
    from app.services.chat.session import ChatSession


@dataclass
class Bot:
    id: UUID
    account_id: UUID
    platform: PlatformType
    # is_active: bool
    # persona_name: str
    # system_prompt: str
    # credentials: dict
    # escalation_config: dict | None
    # created_at: datetime

    @classmethod
    async def get(cls, bot_id: UUID, repo: BotRepository) -> Bot: ...

    @classmethod
    async def create(cls, account_id: UUID, platform: PlatformType, repo: BotRepository, **kwargs) -> Bot: ...

    async def process(self, chat: ChatSession, llm: LLMClient) -> str: ...
