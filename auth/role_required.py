from functools import wraps
from quart import request, jsonify
from quart_auth import current_user, login_required

from db_function.user_function import user_has_role


def role_required(role_name):
    def decorator(f):
        @wraps(f)
        @login_required
        async def decorated_function(*args, **kwargs):
            user_id = current_user.auth_id  # используем auth_id для получения id пользователя

            # admin везде имеет доступ
            if user_has_role(user_id, 'admin'):
                return await f(*args, **kwargs)

            # если это HR officer routes, то head physician тоже имеет доступ
            if role_name == 'hr officer' and user_has_role(user_id, 'head physician'):
                return await f(*args, **kwargs)

            if user_has_role(user_id, role_name):
                return await f(*args, **kwargs)

            return jsonify({"message": f"Access forbidden: {role_name.capitalize()}s only"}), 403

        return decorated_function
    return decorator
