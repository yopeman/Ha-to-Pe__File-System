import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Enum, DateTime

from models import Base


class UserRoles(enum.Enum):
    USER = 'user'
    ADMIN = 'admin'

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRoles), default=UserRoles.USER, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime)
