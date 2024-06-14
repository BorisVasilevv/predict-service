from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


class ScheduleRecord(Base):
    class ScheduleRecord(Base):
        __tablename__ = 'schedule_record'
        id = Column(Integer, primary_key=True)
        doctor_id = Column(Integer, ForeignKey('doctor.id'))
        examination_id = Column(Integer, ForeignKey('examination.id'))
        doctor = relationship("Doctor", back_populates="schedule_records")
        examination = relationship("Examination", back_populates="schedule_record")


