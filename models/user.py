from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)

    role = relationship("Role", back_populates="users")

    def has_permission(self, permission):
        return permission in self.role.permissions.split(',')
