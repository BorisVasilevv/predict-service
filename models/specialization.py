from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.association import doctor_specialization


class Specialization(Base):
    __tablename__ = 'specialization'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # Связь с таблицей докторов
    doctors = relationship("Doctor", secondary=doctor_specialization, back_populates="specializations")
