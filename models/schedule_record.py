from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.address import Address
from models.base import Base
from models.user_specialization import user_specialization


class ScheduleRecord(Base):
    __tablename__ = 'schedule_record'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('examination.id'))

    # Связь с таблицей адресов
    address = relationship("Address", back_populates="user")
