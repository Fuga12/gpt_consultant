"""Импортируйте сюда ORM-модули доменов, чтобы Atlas увидел все таблицы."""

from app.db.base import Base
from app.services.accounts.model import AccountModel  # noqa: F401
from app.services.bots.model import BotModel  # noqa: F401

__all__ = ["Base"]
