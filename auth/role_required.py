from functools import wraps
from quart import request, jsonify
from quart_auth import current_user, AuthUser, login_required

from db_function.user_function import user_has_role


def role_required(role_name):
    def decorator(f):
        @wraps(f)
        @login_required
        async def decorated_function(*args, **kwargs):
            user_id = current_user.auth_id  # Используем auth_id для получения id пользователя
            if user_has_role(user_id, role_name):
                return await f(*args, **kwargs)
            return jsonify({"message": "Access forbidden: Admins only"}), 403
        return decorated_function
    return decorator
