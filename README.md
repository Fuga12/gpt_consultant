# GPT Consultant

Прототип backend-сервиса для Telegram-ассистентов с настраиваемыми системными промптами и ответами YandexGPT. Python, Litestar и асинхронный доступ к PostgreSQL.

Проект показывает интеграцию HTTP API, LLM-клиента, платформы сообщений и слоя хранения. Это прототип: авторизация HTTP API, постоянная история диалогов и автоматические тесты пока не реализованы.

## Возможности

- Прямой HTTP-запрос к YandexGPT без Telegram.
- Получение текстовых сообщений в личных чатах Telegram и отправка ответа модели.
- Аккаунты и настройки ботов в PostgreSQL: платформа, системный промпт, активность и учётные данные.
- Обновление системного промпта бота через API.
- Асинхронный клиент Yandex Foundation Models: запуск операции, опрос результата и таймаут ожидания.
- Разделение доменной логики, репозиториев, платформ сообщений и LLM-клиента.
- Профили `dev`, `stable`, `dummy`, Docker Compose и начальная SQL-миграция.

## Стек

| Область | Технологии |
| --- | --- |
| API | Python 3.12+, Litestar, Pydantic Settings, Uvicorn |
| Данные | PostgreSQL 18, SQLAlchemy 2, asyncpg |
| Интеграции | HTTPX, Yandex Foundation Models, Pyrogram |
| Разработка | uv, Ruff, Docker Compose, Atlas |

## Устройство

```text
Telegram → Pyrogram → BotManager → Bot → LLMClient → YandexGPT
                          │
                          └── AccountRepository / BotRepository → PostgreSQL

HTTP POST /llm/complete ─────────────────→ LLMClient → YandexGPT
HTTP PATCH /bots/{bot_id}/system-prompt ─→ BotRepository → PostgreSQL
```

`LLMClient` задаёт контракт модели, `Platform` — контракт платформы сообщений. Реализованы YandexGPT и Telegram. `BotManager` связывает аккаунт, активного бота, входящее сообщение и отправку ответа. Клиенты и соединения закрываются при завершении приложения.

## Быстрый старт

Нужны Docker и Docker Compose с поддержкой `include`.

```bash
git clone https://github.com/Fuga12/gpt_consultant.git
cd gpt_consultant
cp backend/.example.env backend/.env
```

В `backend/.env` задайте пароль локальной БД. Для реальных ответов модели также нужны собственные `APP_YAGPT__API_KEY` и `APP_YAGPT__FOLDER_ID`:

```dotenv
APP_PROFILE=dev
APP_DATABASE__HOST=postgres
APP_DATABASE__PORT=5432
APP_DATABASE__USER=app
APP_DATABASE__PASSWORD=replace_with_local_password
APP_DATABASE__NAME=app_dev
APP_PORT=8000
APP_YAGPT__API_KEY=
APP_YAGPT__FOLDER_ID=
```

```bash
docker compose up --build
```

Compose запускает PostgreSQL и API на порту `8000`. При запуске контейнера приложения применяется идемпотентная начальная SQL-миграция. Ключ модели нужен для LLM-запросов; пустая база не запускает Telegram-клиентов.

**API не имеет авторизации.** Используйте локальную среду; не публикуйте порт приложения в интернете. Запросы к модели используют ваш аккаунт Yandex Cloud и его тарификацию.

### API

| Метод | Путь | Назначение |
| --- | --- | --- |
| `POST` | `/llm/complete` | Ответ модели на сообщение с необязательным системным промптом |
| `PATCH` | `/bots/{bot_id}/system-prompt` | Изменение промпта существующего бота |

```bash
curl -X POST http://localhost:8000/llm/complete \
  -H 'Content-Type: application/json' \
  -d '{"message":"Что такое ETL?","system_prompt":"Объясняй кратко и по существу."}'
```

Успешный ответ имеет вид `{"text": "..."}`. В профиле `dummy` LLM-клиент отключён, endpoint возвращает `503`.

```bash
curl -X PATCH http://localhost:8000/bots/00000000-0000-0000-0000-000000000002/system-prompt \
  -H 'Content-Type: application/json' \
  -d '{"system_prompt":"Ты помощник по продукту. Отвечай кратко."}'
```

Для второго примера в БД должна существовать запись бота с указанным UUID. Иначе API вернёт `404`.

### Telegram

В [`backend/scripts/seed_test_user.sql`](backend/scripts/seed_test_user.sql) находится шаблон аккаунта и бота с демонстрационными значениями.

1. Создайте локальную копию SQL-шаблона вне Git и подставьте собственные `api_id`, `api_hash` и `bot_token`.
2. Примените её к локальной БД после запуска стека.
3. Перезапустите приложение: активные боты загружаются при старте.

Без настоящих Telegram-учётных данных не применяйте шаблон с `is_active=true`: приложение попытается запустить такого бота. Ключи и файлы сессий Pyrogram не должны попадать в Git.

## Разработка без Docker

Нужны Python 3.12+ и uv. Для проверки запуска без PostgreSQL и внешних API используйте `dummy`:

```bash
cd backend
uv sync --frozen
APP_PROFILE=dummy uv run uvicorn app.app:app --host 127.0.0.1 --port 8000
```

Для полноценного `dev`-режима нужна PostgreSQL с применённой схемой. При локальном запуске укажите в `.env` адрес вашей БД, например `APP_DATABASE__HOST=localhost`.

Описание настроек, Atlas и конфигурации редактора: [`backend/README.md`](backend/README.md).

## Структура

```text
backend/
├── app/api/          # HTTP-обработчики
├── app/clients/      # YandexGPT и запуск Telegram-клиентов
├── app/config/       # Настройки и профили
├── app/db/           # Движок и сессии SQLAlchemy
├── app/migrations/   # SQL-схема и регистр моделей для Atlas
├── app/services/     # Аккаунты, боты, диалоги и контракты интеграций
├── scripts/          # Демонстрационный SQL-шаблон
└── docker/           # Запуск приложения в контейнере
```

## Ограничения и следующие шаги

- HTTP API не проверяет пользователя и права доступа; перед развёртыванием общего сервиса нужны авторизация и изоляция аккаунтов.
- История Telegram-диалога пока не загружается: `fetch_history()` возвращает пустой список. Ответ учитывает текущий запрос и системный промпт.
- Учётные данные ботов хранятся в JSONB без шифрования на уровне приложения. Для эксплуатации нужен отдельный механизм управления секретами.
- Создание аккаунтов и ботов выполняется через слой репозиториев или SQL; публичного CRUD API пока нет.
- Поле `escalation_config` заложено в схему, но передача диалога оператору не реализована.
- Нет RAG, вызова инструментов или агентного планирования. Текущая реализация — LLM-ассистент.
- Автоматических тестов и CI пока нет. Следующие приоритеты: тесты LLM-клиента с подменой HTTP, проверки API и сценарии отказов Telegram.
