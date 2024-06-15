from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base import Base

user_specialization = Table('user_specialization', Base.metadata,
                            Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
                            Column('specialization_id', Integer, ForeignKey('specialization.id'),
                                   primary_key=True)
                            )
