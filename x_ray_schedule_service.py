import asyncio
import secrets

from quart import Quart, request, jsonify, render_template, redirect, url_for, flash
from quart_auth import QuartAuth, AuthUser, login_user, logout_user, login_required, current_user
from quart_cors import cors, route_cors
from hypercorn.config import Config
from hypercorn.asyncio import serve

import logging
from logging import INFO

from auth.CustomUserAuth import CustomAuthUser
from auth.role_required import role_required
from config.environment import secret_key
from db_function.doctor_function import add_doctor, delete_doctor_by_id, get_all_doctors, get_doctor_by_id, \
    update_doctor
from db_function.email_function import send_confirmation_email
from db_function.specialization_function import get_all_specializations, get_specializations_by_doctor_id
from db_function.user_function import authenticate_user, create_pending_user
from models.base import Session
from models.pending_user import PendingUser
from models.user import User

app = Quart(__name__, template_folder='view/templates')
quart_auth = QuartAuth(app)
app.secret_key = secret_key
logger = logging.getLogger()


def __config_logger():
    file_log = logging.FileHandler('x_ray_schedule_service.log')
    console_log = logging.StreamHandler()
    FORMAT = '[%(levelname)s] %(asctime)s : %(message)s | %(filename)s'
    logging.basicConfig(level=INFO,
                        format=FORMAT,
                        handlers=(file_log, console_log),
                        datefmt='%d-%m-%y - %H:%M:%S')


# Настройка CORS
app = cors(
    app,
    allow_origin="*",
    allow_credentials=False,  # Нужно отключить если используется '*'
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],  # Разрешенные методы
    allow_headers=["Content-Type", "Authorization"],  # Разрешенные заголовки
)


@app.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'POST':
        data = await request.form
        username = data['username']
        password = data['password']
        email = data['email']

        try:
            token = create_pending_user(username, password, email)
            await send_confirmation_email(email, token)
            await flash('Пожалуйста, подтвердите вашу регистрацию, перейдя по ссылке в отправленном письме.')
            return await render_template('register.html')
        except ValueError as e:
            await flash(str(e))
            return await render_template('register.html')

    return await render_template('register.html')


@app.route('/confirm/<token>')
async def confirm_email(token):
    session = Session()
    pending_user = session.query(PendingUser).filter_by(token=token).first()
    if pending_user:
        new_user = User(username=pending_user.username, password=pending_user.password, email=pending_user.email)
        session.add(new_user)
        session.delete(pending_user)
        session.commit()
        await flash('Ваша учетная запись успешно подтверждена.')
        return redirect(url_for('login'))
    else:
        await flash('Неверный или истекший токен.')
        return redirect(url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'GET':
        return await render_template('login.html')

    elif request.method == 'POST':
        data = await request.form
        username = data.get('username')
        password = data.get('password')

        user = authenticate_user(username, password)
        if user:
            auth_user = CustomAuthUser(user.id)  # Используем CustomAuthUser
            login_user(auth_user)
            return jsonify({"message": "Login successful"}), 200
        return jsonify({"message": "Invalid credentials"}), 401


@app.route('/logout', methods=['POST'])
@login_required
async def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200


@app.route('/add_doctor', methods=['POST', 'GET'])
@role_required('admin')
async def add_doctor_route():
    if request.method == 'GET':
        all_specializations = get_all_specializations()
        return await render_template('add_doctor.html', all_specializations=all_specializations)

    if request.method == 'POST':
        try:
            data = await request.get_json()
            result = add_doctor(data)
            if 'error' in result:
                logger.error(result)
                return jsonify(result), 400
            return jsonify(result), 201
        except Exception as e:
            logger.error(str(e))
            return jsonify({'error': str(e)}), 400


@app.route('/delete_doctor/<int:doctor_id>', methods=['DELETE'])
async def delete_doctor(doctor_id):
    try:
        result = delete_doctor_by_id(doctor_id)
        if result:
            return jsonify({"message": "Doctor deleted successfully"}), 200
        else:
            logger.error("Doctor not found")
            return jsonify({"message": "Doctor not found"}), 404
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@app.route('/doctors', methods=['GET'])
async def list_doctors():
    doctors = get_all_doctors()
    return await render_template('doctors.html', doctors=doctors)


@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'PUT'])
async def edit_doctor_route(doctor_id):
    if request.method == 'GET':
        doctor = get_doctor_by_id(doctor_id)
        all_specializations = get_all_specializations()
        doctor_specializations = get_specializations_by_doctor_id(doctor_id)
        print(doctor_specializations)
        return await render_template('edit_doctor.html', doctor=doctor, all_specializations=all_specializations, doctor_specializations=doctor_specializations)

    if request.method == 'PUT':
        data = await request.get_json()
        try:
            result = await update_doctor(doctor_id, data)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    __config_logger()

    config = Config()
    config.bind = ["0.0.0.0:7777"]
    config.scheme = "https"
    asyncio.run(serve(app, config))
