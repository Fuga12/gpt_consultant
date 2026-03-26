from collections.abc import AsyncGenerator

from litestar.connection import Request
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from app.db.errors import DatabaseNotConfiguredError


def make_session_maker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_db_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    session_maker = request.app.state.session_maker
    if session_maker is None:
        raise DatabaseNotConfiguredError()
    async with session_maker() as session:
        yield session
