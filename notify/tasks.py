import asyncio
from celery import Celery
from notify.database import AsyncSessionLocal
from notify.crud import get_notification_by_id, create_notification_log
from notify.services import EMAIL_RE, send_email, send_telegram_message
import os
from dotenv import load_dotenv


load_dotenv()

# Настройка подключения к брокеру и бэкенду для celery:
celery = Celery(
    __name__,
    broker=os.getenv("CELERY_BROKER_URL"),
    backend=os.getenv("CELERY_RESULT_BACKEND"),
)


@celery.task
def send_notification_task(notification_id: int):
    """ Задача, внутри которой мы запускаем асинхронную логику. """
    return asyncio.run(_process_notification(notification_id))


async def _process_notification(notification_id: int):
    """
    Основная асинхронная логика отправки:
    1. Получаем уведомление из БД
    2. Проверяем, email это или telegram
    3. Отправляем
    4. Пишем лог
    """
    async with AsyncSessionLocal() as db:
        notif = await get_notification_by_id(db, notification_id)
        if not notif:
            return "Нет записей"

        try:
            if EMAIL_RE.match(notif.recipient):
                await send_email(notif.recipient, "Уведомление", notif.message_text, notif.delay)
            else:
                await send_telegram_message(notif.recipient, notif.message_text, notif.delay)
            await create_notification_log(db, notif.id, status="SUCCESS")
            return f"Уведомление {notif.id} успешно отправлено."

        except Exception as e:
            await create_notification_log(db, notif.id, status="FAILED", error_message=str(e))
            return f"Ошибка при отправке уведомления {notif.id}: {str(e)}"
