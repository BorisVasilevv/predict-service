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
from db_function.email_function import send_confirmation_email, confirm_pending_user, send_reset_password_email
from db_function.specialization_function import get_all_specializations, get_specializations_by_user_id
from db_function.user_function import authenticate_user, create_pending_user, get_all_users, assign_role_to_user, \
    get_all_roles, remove_role_from_user, delete_user_by_id, get_user_by_id, update_user, get_user_by_email, \
    update_user_password, save_confirmation_code
from models.base import Session
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


@app.route('/users')
async def list_users():
    users = get_all_users()
    roles = get_all_roles()
    return await render_template('users.html', users=users, roles=roles)


@app.post('/assign_role')
async def assign_role():
    data = await request.form
    user_id = data.get('user_id')
    role_name = data.get('role')

    try:
        assign_role_to_user(int(user_id), role_name)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return redirect(url_for('list_users'))


@app.post('/remove_role')
async def remove_role():
    data = await request.form
    user_id = data.get('user_id')

    try:
        remove_role_from_user(int(user_id))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return redirect(url_for('list_users'))


@app.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'POST':
        data = await request.form
        username = data['username']
        password = data['password']
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']
        patronymic = data.get('patronymic')
        phone_number = data['phone_number']
        street = data['street']
        house = data['house']
        flat = data.get('flat')
        city = data['city']
        region = data.get('region')
        zip_code = data['zip_code']
        specializations = data.getlist('specializations')

        try:
            token = create_pending_user(
                username, password, email, first_name, last_name,
                patronymic, phone_number, street, house, flat, city,
                region, zip_code, specializations
            )
            await send_confirmation_email(email, token)
            await flash('Пожалуйста, подтвердите вашу регистрацию, перейдя по ссылке в отправленном письме.')
            return await render_template('register.html')
        except ValueError as e:
            await flash(str(e), 'error')
            return await render_template('register.html')

    all_specializations = get_all_specializations()
    return await render_template('register.html', all_specializations=all_specializations)


@app.route('/confirm/<token>')
async def confirm_email(token):
    if confirm_pending_user(token):
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


@app.route('/forgot-password', methods=['GET', 'POST'])
async def forgot_password():
    if request.method == 'POST':
        data = await request.form
        email = data['email']

        user = get_user_by_email(email)
        if user:
            confirmation_code = secrets.token_urlsafe(6)  # Генерируем код подтверждения
            save_confirmation_code(email, confirmation_code)
            await send_reset_password_email(email, confirmation_code)
            await flash('Код подтверждения отправлен на вашу электронную почту.')
            return redirect(url_for('reset_password'))
        else:
            await flash('Пользователь с таким email не найден.')
            return await render_template('forgot_password.html')

    return await render_template('forgot_password.html')


@app.route('/reset-password', methods=['GET', 'POST'])
async def reset_password():
    if request.method == 'POST':
        data = await request.form
        email = data['email']
        confirmation_code = data['confirmation_code']
        new_password = data['new_password']

        user = get_user_by_email(email)
        if user and user.confirmation_code == confirmation_code:
            update_user_password(email, new_password)
            await flash('Пароль успешно сброшен. Теперь вы можете войти с новым паролем.')
            return redirect(url_for('login'))
        else:
            await flash('Неверный код подтверждения или email.')
            return await render_template('reset_password.html')

    return await render_template('reset_password.html')


@app.route('/logout', methods=['GET'])
@login_required
async def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200


@app.route('/delete_user/<int:user_id>', methods=['POST'])
async def delete_user(user_id):
    try:
        result = delete_user_by_id(user_id)
        if result:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@app.route('/edit_user/<int:user_id>', methods=['GET', 'PUT'])
@role_required('hr officer')
async def edit_user_route(user_id):
    if request.method == 'GET':
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        all_specializations = get_all_specializations()
        user_specializations = get_specializations_by_user_id(user_id)
        return await render_template('edit_user.html', user=user, all_specializations=all_specializations,
                                     user_specializations=user_specializations)

    if request.method == 'PUT':
        data = await request.get_json()
        try:
            result = update_user(user_id, data)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    __config_logger()

    config = Config()
    config.bind = ["0.0.0.0:7777"]
    config.scheme = "https"
    asyncio.run(serve(app, config))
