import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime, UniqueConstraint

from models import Base


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"
    id = Column(String, primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    provider = Column(String, nullable=False)
    provider_user_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "provider"),
        UniqueConstraint("provider", "provider_user_id"),
    )