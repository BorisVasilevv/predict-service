from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .association import doctor_specialization


class Specialization(Base):
    __tablename__ = 'specialization'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    # Связь с таблицей докторов
    doctors = relationship("Doctor", secondary=doctor_specialization, back_populates="specializations")

    examinations = relationship(
        "Examination",
        back_populates="specialization"
    )
