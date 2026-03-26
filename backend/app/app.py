from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.di import Provide

from app.config import settings
from app.db import get_db_session, make_async_engine, make_session_maker


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncGenerator[None, None]:
    if settings.profile == "dummy":
        app.state.engine = None
        app.state.session_maker = None
        yield
        return

    engine = make_async_engine(settings)
    session_maker = make_session_maker(engine)
    app.state.engine = engine
    app.state.session_maker = session_maker
    try:
        yield
    finally:
        await engine.dispose()


def create_app() -> Litestar:
    return Litestar(
        debug=settings.debug,
        state={"settings": settings},
        lifespan=[lifespan],
        dependencies={"db_session": Provide(get_db_session)},
    )


app = create_app()
