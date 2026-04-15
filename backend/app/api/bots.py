from uuid import UUID

from litestar import patch
from litestar.exceptions import NotFoundException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.bots.repository import BotRepository


class SystemPromptBody(BaseModel):
    system_prompt: str


@patch("/bots/{bot_id:uuid}/system-prompt")
async def update_bot_system_prompt(
    bot_id: UUID,
    data: SystemPromptBody,
    db_session: AsyncSession,
) -> dict[str, bool]:
    repo = BotRepository(db_session)
    try:
        await repo.update_system_prompt(bot_id, data.system_prompt)
    except ValueError as e:
        raise NotFoundException(detail=str(e)) from e
    await db_session.commit()
    return {"ok": True}
