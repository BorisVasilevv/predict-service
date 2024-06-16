from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.user_specialization import user_specialization
from models.base import Base
from models.role import Role


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=True)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=False)
    phone_number = Column(String(12), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))
    confirmation_code = Column(String(50), nullable=True)

    # Связь с таблицей адресов
    address = relationship("Address", back_populates="user")

    # Связь с таблицей специализаций
    specializations = relationship("Specialization", secondary=user_specialization, back_populates="users")

    role = relationship("Role", back_populates="users")
