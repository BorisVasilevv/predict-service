import asyncio
from quart import Quart, request, jsonify
from quart_cors import cors, route_cors
from hypercorn.config import Config
from hypercorn.asyncio import serve
from db_query_functions import add_doctor, delete_doctor_by_id

import logging
from logging import INFO

app = Quart(__name__)
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
@app.route('/add_doctor', methods=['POST'])
async def add_doctor_route():
    try:
        data = await request.get_json()
        result = add_doctor(data)
        if 'error' in result:
            logger.info(result)
            return jsonify(result), 400
        return jsonify(result), 201
    except Exception as e:
        logger.error({'error': str(e)})
        return jsonify({'error': str(e)}), 400


@app.route('/delete_doctor/<int:doctor_id>', methods=['DELETE'])
async def delete_doctor(doctor_id):
    try:
        result = delete_doctor_by_id(doctor_id)
        if result:
            return jsonify({"message": "Doctor deleted successfully"}), 200
        else:
            return jsonify({"message": "Doctor not found"}), 404
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    __config_logger()

    config = Config()
    config.bind = ["0.0.0.0:7777"]
    config.scheme = "https"
    asyncio.run(serve(app, config))
