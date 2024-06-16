from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base


class TypeKU(Base):
    __tablename__ = 'type_ku'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    examination_types = relationship("ExaminationType", back_populates="typeKU")
