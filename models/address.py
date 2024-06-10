from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    house = Column(String(5), nullable=False)
    street = Column(String(50), nullable=False)
    flat = Column(String(5), nullable=True)
    city = Column(String(50), nullable=False)
    region = Column(String(100), nullable=True)
    zip_code = Column(String(10), nullable=False)

    # Связь с таблицей докторов
    doctor = relationship("Doctor", uselist=False, back_populates="address")
