from typing import Literal

from app.config.abc import AppSettings, DatabaseSettings


class StableDatabaseSettings(DatabaseSettings):
    name: str = "app_stable"
    host: str = "localhost"
    port: int = 5432
    user: str = ""
    password: str = ""


class StableSettings(AppSettings):
    profile: Literal["stable"] = "stable"
    debug: bool = False
    database: DatabaseSettings = StableDatabaseSettings()
