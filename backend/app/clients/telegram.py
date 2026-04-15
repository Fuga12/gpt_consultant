from __future__ import annotations

import logging
from uuid import UUID

from litestar import Litestar
from pyrogram import Client, filters

from app.services.accounts.repository import AccountRepository
from app.services.bots.bot import Bot
from app.services.bots.manager import BotManager
from app.services.bots.repository import BotRepository
from app.services.platforms.base import PlatformFactory, PlatformType

logger = logging.getLogger(__name__)


class TelegramRegistry:
    """Реестр pyrogram.Client по bot_token (для send_message в Platform)."""

    def __init__(self) -> None:
        self._by_token: dict[str, Client] = {}

    def register(self, bot_token: str, client: Client) -> None:
        self._by_token[bot_token] = client

    def client_for_credentials(self, credentials: dict) -> Client:
        token = credentials["bot_token"]
        return self._by_token[token]

    async def stop_all(self) -> None:
        for c in self._by_token.values():
            try:
                await c.stop()
            except Exception:
                logger.exception("Failed to stop Telegram client")
        self._by_token.clear()


async def setup_telegram_bots(app: Litestar, registry: TelegramRegistry) -> None:
    session_maker = app.state.session_maker
    llm = app.state.llm_client

    async with session_maker() as session:
        repo = BotRepository(session)
        bots = await repo.list_active_by_platform(PlatformType.TELEGRAM)

    for bot in bots:
        await _start_one_bot(registry, bot, session_maker, llm)


async def _start_one_bot(
    registry: TelegramRegistry,
    bot: Bot,
    session_maker,
    llm,
) -> None:
    creds = bot.credentials
    api_id = int(creds["api_id"])
    api_hash = creds["api_hash"]
    bot_token = creds["bot_token"]

    client = Client(
        name=f"bot_{bot.id.hex}",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
    )

    registry.register(bot_token, client)

    account_id: UUID = bot.account_id

    @client.on_message(filters.private & filters.text)
    async def _on_private_text(_c: Client, message) -> None:
        text = message.text or ""
        uid = str(message.from_user.id) if message.from_user else ""
        chat = str(message.chat.id)
        async with session_maker() as session:
            bm = BotManager(
                PlatformFactory,
                llm,
                AccountRepository(session),
                BotRepository(session),
            )
            try:
                await bm.handle_message(
                    PlatformType.TELEGRAM,
                    account_id,
                    chat,
                    uid,
                    user_message=text,
                )
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    await client.start()
    logger.info("Telegram bot started: bot_id=%s", bot.id)
