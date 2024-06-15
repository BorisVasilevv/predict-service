from sqlalchemy.orm import joinedload

from models.base import Session
from models.specialization import Specialization
from models.user import User


def get_all_specializations():
    session = Session()
    try:
        specializations = session.query(Specialization).all()
        return specializations
    finally:
        session.close()


def get_specializations_by_user_id(user_id):
    session = Session()
    try:
        user = session.query(User).options(joinedload(User.specializations)).get(user_id)
        return [specialization.id for specialization in user.specializations]
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
