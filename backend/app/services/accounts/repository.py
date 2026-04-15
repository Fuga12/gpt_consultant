from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.accounts.model import AccountModel

if TYPE_CHECKING:
    from app.services.accounts.account import Account


def _account_from_model(row: AccountModel) -> Account:
    from app.services.accounts.account import Account

    return Account(id=row.id, name=row.name, created_at=row.created_at)


class AccountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, account_id: UUID) -> Account:
        row = await self._session.get(AccountModel, account_id)
        if row is None:
            msg = f"Account {account_id} not found"
            raise ValueError(msg)
        return _account_from_model(row)

    async def create(self, name: str) -> Account:
        model = AccountModel(name=name)
        self._session.add(model)
        await self._session.flush()
        return _account_from_model(model)
