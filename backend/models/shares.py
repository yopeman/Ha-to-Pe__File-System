import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, DateTime, Enum

from models import Base


class InvitationStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    CANCELLED = 'cancelled'
    EXPIRED = 'expired'

class Shares(Base):
    __tablename__ = 'shares'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey('users.id'))
    node_id = Column(String, ForeignKey('nodes.id'), nullable=False)
    group_id = Column(String, ForeignKey('groups.id'), nullable=False)
    status = Column(Enum(InvitationStatus), nullable=False, default=InvitationStatus.PENDING)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    expired_at = Column(DateTime, nullable=False)
    accepted_at = Column(DateTime)
    deleted_at = Column(DateTime)