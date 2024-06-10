from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)

    doctor = relationship('Doctor', back_populates='address', uselist=False)
