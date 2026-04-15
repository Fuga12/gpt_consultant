from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from app.services.bots.repository import BotRepository
from app.services.chat.session import ChatSession
from app.services.clients.llm import LLMClient, LLMMessage
from app.services.platforms.base import PlatformType


@dataclass
class Bot:
    id: UUID
    account_id: UUID
    platform: PlatformType
    is_active: bool
    persona_name: str
    system_prompt: str
    credentials: dict[str, Any]
    escalation_config: dict[str, Any] | None
    created_at: datetime

    @classmethod
    async def get(cls, bot_id: UUID, repo: BotRepository) -> Bot:
        return await repo.get(bot_id)

    @classmethod
    async def create(
        cls,
        account_id: UUID,
        platform: PlatformType,
        repo: BotRepository,
        *,
        credentials: dict[str, Any],
        persona_name: str = "",
        system_prompt: str = "",
        is_active: bool = True,
        escalation_config: dict[str, Any] | None = None,
    ) -> Bot:
        return await repo.create(
            account_id,
            platform,
            persona_name=persona_name,
            system_prompt=system_prompt,
            credentials=credentials,
            is_active=is_active,
            escalation_config=escalation_config,
        )

    async def process(self, chat: ChatSession, llm: LLMClient) -> str:
        messages = [
            LLMMessage(role=m.role, content=m.content) for m in chat.history
        ]
        return await llm.complete(self.system_prompt, messages)
