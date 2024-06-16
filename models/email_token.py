from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from models.base import Base


class EmailToken(Base):
    __tablename__ = 'email_token'

    id = Column(Integer, primary_key=True)
    email = Column(String(50), nullable=False)
    token = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
