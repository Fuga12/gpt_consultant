from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bots.model import BotModel
from app.services.platforms.base import PlatformType

if TYPE_CHECKING:
    from app.services.bots.bot import Bot


def _bot_from_model(row: BotModel) -> Bot:
    from app.services.bots.bot import Bot

    plat = row.platform
    if isinstance(plat, str):
        plat = PlatformType(plat)
    return Bot(
        id=row.id,
        account_id=row.account_id,
        platform=plat,
        is_active=row.is_active,
        persona_name=row.persona_name,
        system_prompt=row.system_prompt,
        credentials=row.credentials,
        escalation_config=row.escalation_config,
        created_at=row.created_at,
    )


class BotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, bot_id: UUID) -> Bot:
        row = await self._session.get(BotModel, bot_id)
        if row is None:
            msg = f"Bot {bot_id} not found"
            raise ValueError(msg)
        return _bot_from_model(row)

    async def get_active(self, account_id: UUID, platform: PlatformType) -> Bot:
        stmt = (
            select(BotModel)
            .where(
                BotModel.account_id == account_id,
                BotModel.platform == platform.value,
                BotModel.is_active.is_(True),
            )
            .limit(1)
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is None:
            msg = f"No active bot for account {account_id} platform {platform.value}"
            raise ValueError(msg)
        return _bot_from_model(row)

    async def create(
        self,
        account_id: UUID,
        platform: PlatformType,
        *,
        persona_name: str = "",
        system_prompt: str = "",
        credentials: dict[str, Any],
        is_active: bool = True,
        escalation_config: dict[str, Any] | None = None,
    ) -> Bot:
        model = BotModel(
            account_id=account_id,
            platform=platform,
            is_active=is_active,
            persona_name=persona_name,
            system_prompt=system_prompt,
            credentials=credentials,
            escalation_config=escalation_config,
        )
        self._session.add(model)
        await self._session.flush()
        return _bot_from_model(model)

    async def update_system_prompt(self, bot_id: UUID, system_prompt: str) -> None:
        stmt = (
            update(BotModel)
            .where(BotModel.id == bot_id)
            .values(system_prompt=system_prompt)
        )
        result = await self._session.execute(stmt)
        if result.rowcount == 0:
            msg = f"Bot {bot_id} not found"
            raise ValueError(msg)

    async def list_active_by_platform(self, platform: PlatformType) -> list[Bot]:
        stmt = select(BotModel).where(
            BotModel.platform == platform.value,
            BotModel.is_active.is_(True),
        )
        result = await self._session.execute(stmt)
        rows = result.scalars().all()
        return [_bot_from_model(r) for r in rows]
