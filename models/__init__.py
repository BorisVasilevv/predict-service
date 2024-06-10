from .base import Base, engine, Session
from .doctor import Doctor
from .specialization import Specialization
from .address import Address

Base.metadata.create_all(engine)
