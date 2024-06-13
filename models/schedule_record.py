from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from .address import Address
from .base import Base
from .association import doctor_specialization


class ScheduleRecord(Base):
    __tablename__ = 'schedule_record'

    id = Column(Integer, primary_key=True)
    examination_id = Column(Integer, ForeignKey('examination.id'))
    doctor_id = Column(Integer, ForeignKey('doctor.id'))

    doctor = relationship(
        "Doctor",
        back_populates="schedule_records"
    )
    examination = relationship(
        "Examination",
        back_populates="schedule_records"
    )


