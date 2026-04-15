-- Тестовый account и telegram-бот. Подставьте свои api_id, api_hash, bot_token в credentials.
-- UUID бота совпадает с примером curl для PATCH system_prompt.

INSERT INTO accounts (id, name, created_at)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Test account',
    now()
);

INSERT INTO bots (
    id,
    account_id,
    platform,
    is_active,
    persona_name,
    system_prompt,
    credentials,
    escalation_config,
    created_at
)
VALUES (
    '00000000-0000-0000-0000-000000000002',
    '00000000-0000-0000-0000-000000000001',
    'telegram',
    true,
    'Test bot',
    'Ты тестовый ассистент. Отвечай кратко.',
    '{"api_id": 12345678, "api_hash": "your_api_hash_here", "bot_token": "123:ABC-your-bot-token"}',
    '{}',
    now()
);

-- Пример обновления промпта (порт из APP_PORT, по умолчанию 8000):
-- curl -sS -X PATCH "http://localhost:8000/bots/00000000-0000-0000-0000-000000000002/system-prompt" \
--   -H "Content-Type: application/json" \
--   -d '{"system_prompt":"Ты вежливый ассистент."}'
