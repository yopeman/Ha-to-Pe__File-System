import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime

from models import Base


class Shares(Base):
    __tablename__ = 'shares'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey('users.id'))
    node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    group_id = Column(String, ForeignKey('groups.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)