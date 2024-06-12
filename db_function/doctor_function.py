from sqlalchemy.orm import joinedload

from models import Session, Doctor, Specialization, Address


def add_doctor(data):
    session = Session()

    try:
        first_name = data['first_name']
        last_name = data['last_name']
        patronymic = data.get('patronymic')  # Nullable field
        phone_number = data['phone_number']
        email = data['email']
        specializations = data['specializations']
        address_data = data['address']

        # Создаем новый адрес
        address = Address(
            street=address_data['street'],
            house=address_data['house'],
            flat=address_data['flat'],
            city=address_data['city'],
            region=address_data['region'],
            zip_code=address_data['zip_code']
        )

        # Создаем нового врача
        doctor = Doctor(
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
            phone_number=phone_number,
            email=email,
            address=address
        )

        # Добавляем специализации
        specialization_objects = session.query(Specialization).filter(Specialization.id.in_(specializations)).all()
        doctor.specializations = specialization_objects

        # Сохраняем в базу данных
        session.add(doctor)
        session.commit()

        return {'message': 'Doctor added successfully'}

    except Exception as e:
        session.rollback()
        return {'error': str(e)}

    finally:
        session.close()


def delete_doctor_by_id(doctor_id: int):
    session = Session()
    try:
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if doctor:
            address = session.query(Address).filter(Address.id == doctor.address_id).first()
            if address:
                session.delete(address)  # Удаление адреса доктора
            session.delete(doctor)  # Удаление самого доктора
            session.commit()
            return True
        else:
            return False
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_doctor_by_id(doctor_id: int):
    session = Session()
    try:
        doctor = session.query(Doctor).options(joinedload(Doctor.specializations), joinedload(Doctor.address)).filter(Doctor.id == doctor_id).first()
        return doctor
    finally:
        session.close()


def get_all_doctors():
    session = Session()
    try:
        doctors = session.query(Doctor).all()
        return doctors
    finally:
        session.close()


def update_doctor(doctor_id: int, data):
    session = Session()
    try:
        doctor = session.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not doctor:
            return {'error': 'Doctor not found'}

        doctor.first_name = data['first_name']
        doctor.last_name = data['last_name']
        doctor.patronymic = data.get('patronymic')
        doctor.phone_number = data['phone_number']
        doctor.email = data.get('email')

        # Обновление специализаций
        specializations = data['specializations']
        specialization_objects = session.query(Specialization).filter(Specialization.id.in_(specializations)).all()
        doctor.specializations = specialization_objects

        # Обновление адреса
        address_data = data['address']
        address = doctor.address
        address.street = address_data['street']
        address.house = address_data['house']
        address.flat = address_data['flat']
        address.city = address_data['city']
        address.region = address_data['region']
        address.zip_code = address_data['zip_code']

        session.commit()
        return {'message': 'Doctor updated successfully'}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
