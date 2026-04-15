from abc import ABC, abstractmethod
from uuid import UUID


class AccountRepository(ABC):
    @abstractmethod
    async def get(self, account_id: UUID) -> "Account": ...

    @abstractmethod
    async def create(self, name: str) -> "Account": ...
