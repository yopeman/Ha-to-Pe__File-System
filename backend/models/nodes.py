import enum
import uuid
from datetime import datetime

from sqlalchemy import String, Column, ForeignKey, Enum, Boolean, DateTime, UniqueConstraint

from models import Base


class NodeTypes(enum.Enum):
    DIRECTORY = 'directory'
    FILE = 'file'
    ZIP = 'zip'

class NodeVisibilities(enum.Enum):
    PRIVATE = 'private'
    SHARED = 'shared'
    PUBLIC = 'public'

class Nodes(Base):
    __tablename__ = "nodes"
    id = Column(String, primary_key=True, default=uuid.uuid4)
    parent_id = Column(String, ForeignKey("nodes.id"))
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(Enum(NodeTypes), nullable=False)
    visibility = Column(Enum(NodeVisibilities), nullable=False)
    is_hidden = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    trashed_at = Column(DateTime)
    deleted_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint("parent_id", "name"),
    )