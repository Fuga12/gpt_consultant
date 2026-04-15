# Базовый проект на litestar для дальнейших начинаний

## Настройка dev окружения
Нам понадобяться:
1. Docker + docker compose

Запуск стека из корня репозитория (если без `sudo` нет доступа к Docker — используйте `sudo`):

```bash
sudo docker compose up --build
```

### Ошибка `password authentication failed for user "app"`

У Postgres в Docker пароль задаётся **только при первом создании** тома с данными. Если вы уже поднимали compose с другим `APP_DATABASE__PASSWORD` в `.env`, старый пароль остался в volume, а новый из `.env` приложение передаёт зря — получите `FATAL: password authentication failed`.

**Вариант А (проще, данные БД сбросятся):**

```bash
sudo docker compose down -v
sudo docker compose up --build
```

**Вариант Б (сохранить данные):** выставить пароль пользователя `app` в Postgres вручную так, чтобы он совпадал с `APP_DATABASE__PASSWORD` в `backend/.env`.

Редактор: общие настройки VS Code / Cursor и отладка описаны в [backend/README.md](backend/README.md) (раздел «VS Code / Cursor»).
