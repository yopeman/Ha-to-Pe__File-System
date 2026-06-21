import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Enum, DateTime

from models import Base


class InvitationStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    EXPIRED = 'expired'

class Invitations(Base):
    __tablename__ = 'invitations'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    node_id = Column(String, ForeignKey("nodes.id"), nullable=False)
    invited_by = Column(String, ForeignKey("users.id"), nullable=False)
    invited_user = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(InvitationStatus), nullable=False, default=InvitationStatus.PENDING)
    expired_at = Column(DateTime)
    accepted_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)