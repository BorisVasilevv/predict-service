from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base
from models.pending_user_specialization import pending_user_specialization
from models.user_specialization import user_specialization


class Specialization(Base):
    __tablename__ = 'specialization'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    users = relationship("User", secondary=user_specialization, back_populates="specializations")
    pending_users = relationship("PendingUser", secondary=pending_user_specialization, back_populates="specializations")

    examination_types = relationship("ExaminationType", back_populates="specialization")
