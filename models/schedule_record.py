from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .address import Address
from .base import Base
from .association import doctor_specialization


class ScheduleRecord(Base):
    __tablename__ = 'schedule_record'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('examination.id'))

    # Связь с таблицей адресов
    address = relationship("Address", back_populates="doctor")