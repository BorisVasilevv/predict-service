from models.doctor import Doctor
from models.user import User
from models.examination import Examination
from models.role import Role
from models.schedule_record import ScheduleRecord
from models.address import Address
from models.specialization import Specialization
from models.association import doctor_specialization
from models.email_token import EmailToken
from models.pending_user import PendingUser
from models.base import Base, engine, Session

Base.metadata.create_all(engine)
