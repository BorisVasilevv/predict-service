import asyncio
from quart import Quart, request, jsonify, render_template, redirect, url_for
from quart_auth import QuartAuth, AuthUser, login_user, logout_user, login_required, current_user
from quart_cors import cors, route_cors
from hypercorn.config import Config
from hypercorn.asyncio import serve
from db_query_functions import add_doctor, delete_doctor_by_id, get_all_doctors, get_doctor_by_id, update_doctor, \
    get_all_specializations, get_specializations_by_doctor_id

import logging
from logging import INFO
from config.enviroment import secret_key

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


# @route_cors(allow_origin="*")  # Разрешаем все источники для этого маршрута
# Маршрут для добавления нового врача
@app.route('/add_doctor', methods=['POST', 'GET'])
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
