from typing import Literal

from pydantic import Field

from app.config.abc import AppSettings, DatabaseSettings


class DummySettings(AppSettings):
    profile: Literal["dummy"] = "dummy"
    debug: bool = True
    port: int = 8000
    # Заглушка под PostgreSQL; в lifespan к БД не подключаемся.
    database: DatabaseSettings = Field(
        default_factory=lambda: DatabaseSettings(name="app_dummy"),
    )
