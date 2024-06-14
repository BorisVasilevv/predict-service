from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from base import Base


class Examination_Type(Base):
    __tablename__ = 'examination_type'
    id = Column(Integer, primary_key=True)
    specialization_id = Column(Integer, ForeignKey('specialization.id'))
    type_KU_id = Column(Integer, ForeignKey('type_ku.id'))
    max_per_day = Column(Float)
    min_per_day = Column(Float)
    specialization = relationship("Specialization", back_populates="examination_types")
    type_KU = relationship("Type_KU", back_populates="examination_types")
    examinations = relationship("Examination", back_populates="examination_type")