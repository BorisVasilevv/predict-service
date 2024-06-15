from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=True)

    role = relationship("Role", back_populates="users")

    doctor = relationship("Doctor", back_populates="user")
