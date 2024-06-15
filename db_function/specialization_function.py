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


def get_specializations_by_user_id(doctor_id):
    session = Session()

    try:
        # Находим доктора по его ID
        doctor = session.query(User).filter_by(id=doctor_id).first()
        if doctor:
            # Если доктор найден, возвращаем ID его специализаций
            return [specialization.id for specialization in doctor.specializations]
        else:
            # Если доктор не найден, возвращаем пустой список
            return []
    finally:
        session.close()
