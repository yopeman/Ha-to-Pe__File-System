from datetime import datetime

from sqlalchemy import Column, Integer, DateTime

from models import Base


class Settings(Base):
    __tablename__ = "settings"
    free_storage_gb = Column(Integer, nullable=False, default=0)
    price_per_gb = Column(Integer, nullable=False, default=0)
    trash_retention_days = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)