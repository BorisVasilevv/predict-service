from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base import Base

pending_user_specialization = Table('pending_user_specialization', Base.metadata,
                                    Column('pending_user_id', Integer, ForeignKey('pending_user.id'), primary_key=True),
                                    Column('specialization_id', Integer, ForeignKey('specialization.id'),
                                           primary_key=True)
                                    )
