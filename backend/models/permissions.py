import uuid
from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime

from models import Base


class Permissions(Base):
    __tablename__ = 'permissions'
    id = Column(String, primary_key=True, default=uuid.uuid4)
    group_id = Column(String, ForeignKey('groups.id'), nullable=False, unique=True)
    list = Column(Boolean, nullable=False, default=False)
    read = Column(Boolean, nullable=False, default=False)
    write = Column(Boolean, nullable=False, default=False)
    read_metadata = Column(Boolean, nullable=False, default=False)
    create_file = Column(Boolean, nullable=False, default=False)
    create_directory = Column(Boolean, nullable=False, default=False)
    rename = Column(Boolean, nullable=False, default=False)
    move = Column(Boolean, nullable=False, default=False)
    copy = Column(Boolean, nullable=False, default=False)
    delete = Column(Boolean, nullable=False, default=False)
    restore = Column(Boolean, nullable=False, default=False)
    purge = Column(Boolean, nullable=False, default=False)
    download = Column(Boolean, nullable=False, default=False)
    upload = Column(Boolean, nullable=False, default=False)
    zip = Column(Boolean, nullable=False, default=False)
    share = Column(Boolean, nullable=False, default=False)
    change_visibility = Column(Boolean, nullable=False, default=False)
    manage_permissions = Column(Boolean, nullable=False, default=False)
    change_owner = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)