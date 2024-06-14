from sqlalchemy import Column, Integer, String
from models.base import Base


class PendingUser(Base):
    __tablename__ = 'pending_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    token = Column(String(50), unique=True, nullable=False)
