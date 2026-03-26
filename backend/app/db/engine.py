from urllib.parse import quote_plus

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.config.abc import AppSettings


def make_async_engine(settings: AppSettings) -> AsyncEngine:
    db = settings.database
    auth = f"{quote_plus(db.user)}:{quote_plus(db.password)}"
    url = f"postgresql+asyncpg://{auth}@{db.host}:{db.port}/{db.name}"
    return create_async_engine(
        url,
        echo=settings.debug,
        pool_pre_ping=True,
    )
