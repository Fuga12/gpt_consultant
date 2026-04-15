from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.datastructures import State
from litestar.di import Provide

from app.api.bots import update_bot_system_prompt
from app.api.llm import llm_complete
from app.clients.telegram import TelegramRegistry, setup_telegram_bots
from app.clients.yagpt import YandexFoundationLLMClient
from app.config.settings import settings
from app.db import get_db_session, make_async_engine, make_session_maker
from app.services.platforms.base import PlatformFactory
from app.services.platforms.telegram import TelegramPlatform


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    if settings.profile == "dummy":
        app.state.engine = None
        app.state.session_maker = None
        app.state.llm_client = None
        app.state.telegram_registry = None
        yield
        return

    engine = make_async_engine(settings)
    session_maker = make_session_maker(engine)
    app.state.engine = engine
    app.state.session_maker = session_maker

    llm = YandexFoundationLLMClient(settings.yagpt)
    app.state.llm_client = llm

    registry = TelegramRegistry()
    app.state.telegram_registry = registry
    PlatformFactory.register(TelegramPlatform(registry))

    await setup_telegram_bots(app, registry)

    try:
        yield
    finally:
        await registry.stop_all()
        await llm.aclose()
        await engine.dispose()


def create_app() -> Litestar:
    return Litestar(
        debug=settings.debug,
        state=State({"settings": settings}),
        lifespan=[lifespan],
        dependencies={"db_session": Provide(get_db_session)},
        route_handlers=[update_bot_system_prompt, llm_complete],
    )


app = create_app()
