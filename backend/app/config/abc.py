from abc import ABC

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = ""
    password: str = ""
    name: str = "app"


class AppSettings(BaseSettings, ABC):
    """Схема настроек; значения задают подклассы (dev / stable / dummy)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    profile: str
    debug: bool
    port: int = Field(default=8000, ge=1, le=65535, description="Порт HTTP (uvicorn)")
    database: DatabaseSettings
