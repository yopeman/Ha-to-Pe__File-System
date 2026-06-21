import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, UniqueConstraint

from models import Base


class FileVersions(Base):
    __tablename__ = "file_versions"
    id = Column(String, primary_key=True, default=uuid.uuid4)
    node_id = Column(String, ForeignKey("nodes.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    storage_path = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint("node_id", "version_number"),
    )