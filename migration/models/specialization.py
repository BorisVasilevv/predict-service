from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .association import doctor_specialization

class Specialization(Base):
    __tablename__ = 'specializations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    doctors = relationship('Doctor', secondary=doctor_specialization, back_populates='specializations')
