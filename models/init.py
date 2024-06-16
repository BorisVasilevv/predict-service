from models.user import User
from models.examination import Examination
from models.examination_type import ExaminationType
from models.typeKU import TypeKU
from models.role import Role
from models.schedule_record import ScheduleRecord
from models.address import Address
from models.specialization import Specialization
from models.contingency import Contingency
from models.user_specialization import user_specialization
from models.pending_user_specialization import pending_user_specialization
from models.email_token import EmailToken
from models.pending_user import PendingUser
from models.base import Base, engine, Session

Base.metadata.create_all(engine)
