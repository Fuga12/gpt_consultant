from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

from app.services.accounts.repository import AccountRepository
from app.services.platforms.base import PlatformType

if TYPE_CHECKING:
    from app.services.bots.bot import Bot
    from app.services.bots.repository import BotRepository


@dataclass
class Account:
    id: UUID
    # name: str
    # created_at: datetime

    @classmethod
    async def get(cls, account_id: UUID, repo: AccountRepository) -> Account: ...

    @classmethod
    async def create(cls, name: str, repo: AccountRepository) -> Account: ...

    async def get_active_bot(self, platform: PlatformType, repo: BotRepository) -> Bot: ...
