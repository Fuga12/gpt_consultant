import os

from app.config.abc import AppSettings


def get_settings() -> AppSettings:
    profile = os.environ.get("APP_PROFILE", "dev").strip().lower()
    match profile:
        case "stable":
            from app.config.stable import StableSettings

            return StableSettings()
        case "dev":
            from app.config.dev import DevSettings

            return DevSettings()
        case "dummy" | _:
            from app.config.dummy import DummySettings

            return DummySettings()


settings = get_settings()
