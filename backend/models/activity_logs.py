import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON

from models import Base


class ActivityLogs(Base):
    __tablename__ = "activity_logs"
    id = Column(String, primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("users.id"))
    node_id = Column(String, ForeignKey("nodes.id"))
    action = Column(String, nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)