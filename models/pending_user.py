from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.pending_user_specialization import pending_user_specialization
from models.base import Base


class PendingUser(Base):
    __tablename__ = 'pending_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    phone_number = Column(String(12), nullable=False)
    street = Column(String(100), nullable=False)
    house = Column(String(50), nullable=False)
    flat = Column(String(50), nullable=True)
    city = Column(String(100), nullable=False)
    region = Column(String(100), nullable=True)
    zip_code = Column(String(20), nullable=False)
    token = Column(String(50), unique=True, nullable=False)

    # Отношения многие ко многим для специализаций
    specializations = relationship("Specialization", secondary=pending_user_specialization,
                                   back_populates="pending_users")






