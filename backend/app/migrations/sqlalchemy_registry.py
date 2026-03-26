"""Импортируйте сюда ORM-модули доменов, чтобы Atlas увидел все таблицы."""

from app.db.base import Base

__all__ = ["Base"]

# from app.some_domain.models import SomeModel  # noqa: F401
