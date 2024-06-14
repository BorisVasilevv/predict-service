from email.message import EmailMessage

import aiosmtplib
from quart import url_for

from config.environment import gmail_address, gmail_password
from models.base import Session
from models.email_token import EmailToken
from models.user import User


async def send_confirmation_email(email, token):
    message = EmailMessage()
    message["From"] = gmail_address  # Замените на ваш Gmail-адрес
    message["To"] = email
    message["Subject"] = "Код подтверждения регистрации"
    message.set_content(f"Пожалуйста, подтвердите вашу регистрацию, перейдя по следующей ссылке: {url_for('confirm_email', token=token, _external=True)}")

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=gmail_address,
        password=gmail_password)


def verify_token(token: str):
    session = Session()
    email_token = session.query(EmailToken).filter_by(token=token).first()
    if email_token:
        user = session.query(User).filter_by(email=email_token.email).first()
        if user:
            user.is_active = True
            session.delete(email_token)
            session.commit()
            session.close()
            return True
    session.close()
    return False
