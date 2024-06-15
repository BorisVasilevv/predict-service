from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base import Base

doctor_specialization = Table('doctor_specialization', Base.metadata,
                              Column('user_id', Integer, ForeignKey('user.id')),
                              Column('specialization_id', Integer, ForeignKey('specialization.id'))
                              )
