from app.db.base import Base


class BotModel(Base):
    __tablename__ = "bots"
    # id: UUID — primary key
    # account_id: UUID — FK → accounts.id (CASCADE)
    # platform: PlatformType
    # is_active: bool — partial unique index on (account_id, platform) where is_active=true
    # persona_name: str — display name, e.g. "Менеджер Анна"
    # system_prompt: str
    # credentials: dict (JSONB) — platform-specific auth data
    # escalation_config: dict | None (JSONB)
    # created_at: datetime — auto
