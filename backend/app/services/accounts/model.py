from app.db.base import Base


class AccountModel(Base):
    __tablename__ = "accounts"
    # id: UUID — primary key
    # name: str — account name
    # created_at: datetime — auto
