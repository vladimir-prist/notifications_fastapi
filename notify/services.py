import re
import httpx
import aiosmtplib
from email.mime.text import MIMEText
from email.header import Header
from notify.config import (
    EMAIL_HOST,
    EMAIL_PORT,
    EMAIL_USERNAME,
    EMAIL_PASSWORD,
    FROM_EMAIL,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_URL
)


# Регулярка для проверки email:
EMAIL_RE = re.compile(r"(^[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-.]+$)")


async def send_email(to_email: str, subject: str, body: str, delay: int):
    """ Отправляет email на указанный адрес через SMTP. """
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        await aiosmtplib.send(
            msg,
            hostname=EMAIL_HOST,
            port=int(EMAIL_PORT),
            username=EMAIL_USERNAME,
            password=EMAIL_PASSWORD,
            use_tls=False,
            timeout=delay
        )
    except Exception as e:
        raise e


async def send_telegram_message(chat_id: str, text: str, delay: int):
    """ Отправляет сообщение в Telegram пользователю с помощью Бота. """
    url = f"{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        async with httpx.AsyncClient(timeout=delay) as client:
            response = await client.post(url, json=params, timeout=delay)
        if not response.is_success:
            raise Exception(f"Ошибка при отправке сообщения в Telegram: {response.text}")
    except Exception as e:
        raise e


def delay_to_seconds(delay_code: int) -> int:
    """ Отложенная отправка: 0 -> сейчас, 1 -> через 1 час, 2 -> через 24 часа. """
    if delay_code == 1:
        return 3600
    elif delay_code == 2:
        return 86400
    return 0
