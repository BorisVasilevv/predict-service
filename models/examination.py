from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base import Base


class Examination(Base):
    __tablename__ = 'examination'
    id = Column(Integer, primary_key=True)
    examination_type_id = Column(Integer, ForeignKey('examination_type.id'))
    datetime = Column(Date)

    examination_type = relationship("ExaminationType", back_populates="examinations")
    schedule_record = relationship("ScheduleRecord", back_populates="examination", uselist=False)
