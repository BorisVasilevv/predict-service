from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base
from models.association import doctor_specialization


class Doctor(Base):
    __tablename__ = 'doctor'

    id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=False)
    phone_number = Column(String(12), nullable=False)
    email = Column(String(50), nullable=True)
    address_id = Column(Integer, ForeignKey('address.id'))
    role_id = Column(Integer, ForeignKey('role.id'), nullable=True)

    user = relationship("User", back_populates="doctor")

    # Связь с таблицей адресов
    address = relationship("Address", back_populates="doctor")

    # Связь с таблицей специализаций
    specializations = relationship("Specialization", secondary=doctor_specialization, back_populates="doctors")
