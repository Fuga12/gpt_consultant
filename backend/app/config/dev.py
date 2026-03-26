from typing import Literal

from app.config.abc import AppSettings, DatabaseSettings


class DevDatabaseSettings(DatabaseSettings):
    name: str = "app_dev"
    host: str = "localhost"
    port: int = 5432
    user: str = ""
    password: str = ""


class DevSettings(AppSettings):
    profile: Literal["dev"] = "dev"
    debug: bool = True
    database: DatabaseSettings = DevDatabaseSettings()
