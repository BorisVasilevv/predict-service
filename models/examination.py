from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Examination(Base):
    __tablename__ = 'examination'
    id = Column(Integer, primary_key=True)
    examination_type_id = Column(Integer, ForeignKey('examination_type.id'))
    datetime = Column(DateTime)
    examination_type = relationship("Examination_Type", back_populates="examinations")
    schedule_record = relationship("ScheduleRecord", back_populates="examination", uselist=False)

