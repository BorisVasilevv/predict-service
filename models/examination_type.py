from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.base import Base
from models.typeKU import TypeKU


class ExaminationType(Base):
    __tablename__ = 'examination_type'
    id = Column(Integer, primary_key=True)
    specialization_id = Column(Integer, ForeignKey('specialization.id'))
    type_KU_id = Column(Integer, ForeignKey('type_ku.id'))
    max_per_day = Column(Float)
    min_per_day = Column(Float)

    specialization = relationship("Specialization", back_populates="examination_types")
    typeKU = relationship("TypeKU", back_populates="examination_types")
    examinations = relationship("Examination", back_populates="examination_type")
