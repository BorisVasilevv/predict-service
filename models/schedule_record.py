from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from models.examination import Examination

from models.address import Address
from models.base import Base
from models.user_specialization import user_specialization

class ScheduleRecord(Base):
    __tablename__ = 'schedule_record'
    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    examination_id = Column(Integer, ForeignKey('examination.id'))

    doctor = relationship("Doctor", back_populates="schedule_records")

    examination = relationship("Examination", back_populates="schedule_record")


