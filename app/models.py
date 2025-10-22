import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.mysql import BINARY
from datetime import datetime
from .database import Base




def gen_uuid_bin():
    return uuid.uuid4().bytes


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BINARY(16), primary_key=True, default=gen_uuid_bin)
    user_name = Column(String(150), nullable=False)
    user_email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Note(Base):
    __tablename__ = 'notes'
    note_id = Column(BINARY(16), primary_key=True, default=gen_uuid_bin)
    user_id = Column(BINARY(16), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    note_title = Column(String(255), nullable=True)
    note_content = Column(Text, nullable=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    last_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)