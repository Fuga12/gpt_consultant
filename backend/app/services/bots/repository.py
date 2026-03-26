from abc import ABC, abstractmethod
from uuid import UUID

from app.services.platforms.base import PlatformType


class BotRepository(ABC):
    @abstractmethod
    async def get(self, bot_id: UUID) -> "Bot": ...

    @abstractmethod
    async def get_active(self, account_id: UUID, platform: PlatformType) -> "Bot": ...

    @abstractmethod
    async def create(self, account_id: UUID, platform: PlatformType, **kwargs) -> "Bot": ...
