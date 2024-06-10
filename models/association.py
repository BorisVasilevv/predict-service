from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

doctor_specialization = Table('doctor_specialization', Base.metadata,
                              Column('doctor_id', Integer, ForeignKey('doctor.id')),
                              Column('specialization_id', Integer, ForeignKey('specialization.id'))
                              )
