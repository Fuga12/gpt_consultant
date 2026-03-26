from dataclasses import dataclass, field

from app.services.platforms.base import Message, PlatformType


@dataclass
class ChatSession:
    chat_id: str
    platform: PlatformType
    end_user_id: str
    history: list[Message] = field(default_factory=list)
