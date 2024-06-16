from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base import Base
# from models.doctor import Doctor


class Contingency(Base):
    __tablename__ = 'contingency'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    datetime_from = Column(DateTime)
    datetime_to = Column(DateTime)

    doctor = relationship("Doctor", back_populates="contingencies")
