import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, DateTime

from models import Base


class UserStorage(Base):
    __tablename__ = "user_storage"
    id = Column(String, primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("user.id"), nullable=False, unique=True)
    used_bytes = Column(Integer, nullable=False, default=0)
    quota_bytes = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)