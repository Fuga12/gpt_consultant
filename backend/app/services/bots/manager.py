from uuid import UUID

from app.services.accounts.account import Account
from app.services.accounts.repository import AccountRepository
from app.services.bots.repository import BotRepository
from app.services.chat.session import ChatSession
from app.services.clients.llm import LLMClient
from app.services.platforms.base import Message, PlatformFactory, PlatformType


class BotManager:
    def __init__(
        self,
        platform_factory: PlatformFactory,
        llm: LLMClient,
        account_repo: AccountRepository,
        bot_repo: BotRepository,
    ) -> None:
        self._platform_factory = platform_factory
        self._llm = llm
        self._account_repo = account_repo
        self._bot_repo = bot_repo

    async def handle_message(
        self,
        platform_type: PlatformType,
        account_id: UUID,
        chat_id: str,
        end_user_id: str,
        user_message: str,
    ) -> str:
        account = await Account.get(account_id, self._account_repo)
        bot = await account.get_active_bot(platform_type, self._bot_repo)
        platform = self._platform_factory.get(platform_type)

        prior = await platform.fetch_history(chat_id, bot.credentials)
        history = [*prior, Message(role="user", content=user_message)]
        chat = ChatSession(
            chat_id=chat_id,
            platform=platform_type,
            end_user_id=end_user_id,
            history=history,
        )

        response = await bot.process(chat, self._llm)
        await platform.send_message(chat_id, response, bot.credentials)
        return response
