from .base import Base, engine, Session
from .doctor import Doctor
from .specialization import Specialization
from .address import Address
from .user import User
from .role import Role

Base.metadata.create_all(engine)
