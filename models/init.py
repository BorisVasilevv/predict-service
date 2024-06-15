from models.doctor import Doctor
from models.user import User
from models.examination import Examination
from models.examination_type import ExaminationType
from models.typeKU import TypeKU
from models.role import Role
from models.schedule_record import ScheduleRecord
from models.address import Address
from models.specialization import Specialization
from models.association import doctor_specialization
from models.contingency import Contingency
from models.base import Base, engine, Session

Base.metadata.create_all(engine)
