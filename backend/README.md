# Backend (Litestar)

## Конфигурация

- **Схема настроек** — абстрактный [`AppSettings`](app/config/abc.py) (`BaseSettings` + `ABC`): какие поля бывают и как читается окружение (префикс `APP_`, файл `.env`).
- **Профили приложения** — классы в [`app/config/dev.py`](app/config/dev.py), [`app/config/stable.py`](app/config/stable.py), [`app/config/dummy.py`](app/config/dummy.py) с разными дефолтами (`debug`, имя БД и т.д.).
- **`APP_PROFILE`** — какой класс настроек создать: `dev` (по умолчанию), `stable`, `dummy`; неизвестное значение даёт `dummy`. У `dummy` движок БД в lifespan не поднимается (заглушка).
- Подключение к БД только **PostgreSQL** (async через asyncpg); строка подключения в [`app/db/engine.py`](app/db/engine.py) в `make_async_engine`.
- **`get_settings()`** в [`app/config/settings.py`](app/config/settings.py) по `APP_PROFILE` возвращает нужный подкласс; pydantic-settings подмешивает переменные окружения и `.env` поверх дефолтов модели.
- Шаблон переменных: [`.example.env`](.example.env) → скопировать в **`.env`** в этом каталоге (`backend/`, не коммитится).

## Локальный запуск

Из каталога `backend` (где лежат `pyproject.toml` и пакет `app/`):

```bash
uv sync
uv run uvicorn app.app:app --reload
```

Рабочий каталог — `backend`, чтобы находились установленный пакет `app`, `.env` и шаблон настроек.

## Docker

Образ собирается из `backend/Dockerfile`; контекст сборки — каталог `backend` (там же `pyproject.toml` и `app/`).

## Миграции (Atlas)

Схема БД описывается моделями SQLAlchemy; версионные миграции и регистр схемы для Atlas — в [`app/migrations/`](app/migrations/), конфигурация CLI — [`atlas.hcl`](atlas.hcl).

1. **Atlas CLI** — [установка](https://atlasgo.io/getting-started#installation) (например `curl -sSf https://atlasgo.sh | sh`). Нужен **Docker** для `atlas migrate diff --env local` (временный Postgres 18, как в `docker-compose.yml`).
2. **Провайдер** — после `uv sync` доступен `uv run atlas-provider-sqlalchemy` (пакет в dev-зависимостях).
3. **Модели по доменам** — классы таблиц живут в модулях доменов; для Atlas добавляйте импорты в [`app/migrations/sqlalchemy_registry.py`](app/migrations/sqlalchemy_registry.py) (провайдер обходит только этот каталог, без запуска всего `app/`).

Команды из каталога `backend`:

```bash
# сгенерировать новую миграцию по diff моделей и каталога migrations
atlas migrate diff <имя_миграции> --env local

# применить миграции к целевой БД (задайте ATLAS_DATABASE_URL, см. .example.env)
export ATLAS_DATABASE_URL='postgres://user:pass@host:5432/dbname?sslmode=disable'
atlas migrate apply --env apply
```

Подробнее: [Atlas + SQLAlchemy](https://atlasgo.io/guides/orms/sqlalchemy/getting-started).

## VS Code / Cursor

Рекомендуется открывать **корень репозитория** `gpt_consultant`, чтобы сработали пути в [`.vscode/`](../.vscode).

1. Установить предложенные расширения (Python, Ruff).
2. В каталоге `backend`: `uv sync` — появится `.venv`.
3. **Задачи**: `uv: sync`, `ruff: check`, `ruff: format`, `pytest`, `atlas: migrate diff` (подхватывает [`backend/.env`](../.vscode/tasks.json) и спрашивает имя миграции).
4. **Отладка**: `Python: Uvicorn` / `Python: Uvicorn (reload)` — цель `app.app:app`, cwd `backend`.

Линт: `uv run ruff check app` / `uv run ruff format app` (см. `[tool.ruff]` в `pyproject.toml`).
