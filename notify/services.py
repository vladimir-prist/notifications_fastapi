import smtplib
from email.mime.text import MIMEText
from email.header import Header
import requests
from notify.config import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    FROM_EMAIL,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_URL
)


def send_email(to_email: str, subject: str, body: str, delay: int):
    """ Отправляет email на указанный адрес через SMTP. """
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=delay) as server:
            server.ehlo()
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        raise e


def send_telegram_message(chat_id: str, text: str, delay: int):
    """ Отправляет сообщение в Telegram пользователю с помощью Бота. """
    url = f"{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, json=params, timeout=delay)
        if response.status_code != response.ok:
            raise Exception(f"Ошибка при отправке сообщения в Telegram: {response.text}")
    except Exception as e:
        raise e
