from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Type_KU(Base):
    __tablename__ = 'type_ku'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    examination_types = relationship("Examination_Type", back_populates="type_KU")