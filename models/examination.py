from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from .base import Base


class Examination(Base):
    __tablename__ = 'examination'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    specialization_id = Column(Integer, ForeignKey('specialization.id'))


