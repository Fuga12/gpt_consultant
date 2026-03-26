import uvicorn

from app.config.settings import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "app.app:app",
        host="0.0.0.0",
        port=settings.port,
    )


if __name__ == "__main__":
    main()
