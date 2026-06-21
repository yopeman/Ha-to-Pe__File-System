import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime, UniqueConstraint

from models import Base


class Groups(Base):
    __tablename__ = "groups"
    id = Column(String, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint("created_by", "name"),
    )