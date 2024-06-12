from quart_auth import AuthUser, login_user, current_user, logout_user, login_required


class CustomAuthUser(AuthUser):
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(auth_id=str(user_id), *args, **kwargs)  # Устанавливаем auth_id через конструктор

