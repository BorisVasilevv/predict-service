from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .association import doctor_specialization


class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=False)
    phone_number = Column(String(15), unique=True)
    email = Column(String(50), unique=True)

    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship('Address', back_populates='doctor')

    specializations = relationship('Specialization', secondary=doctor_specialization, back_populates='doctors')
