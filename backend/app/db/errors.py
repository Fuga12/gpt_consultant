from litestar.exceptions import ServiceUnavailableException


class DatabaseNotConfiguredError(ServiceUnavailableException):
    """Нет engine/session_maker (профиль dummy)."""

    def __init__(self) -> None:
        super().__init__(detail="База данных в этом профиле не подключена")
