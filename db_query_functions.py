from migration.models import Session, Doctor, Specialization, Address


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
        specialization_objects = session.query(Specialization).filter(Specialization.name.in_(specializations)).all()
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
