from celery import Celery
from sqlalchemy.orm import Session
from notify.database import SessionLocal
from notify.models import Notification, NotificationLog
from notify.services import send_email, send_telegram_message
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
    """ Задача для отправки уведомлений ч/з Celery. """
    db: Session = SessionLocal()
    try:
        notif = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notif:
            return  # Нечего отправлять
        if "@" in notif.recipient:
            send_email(notif.recipient, "New Notification", notif.message_text, notif.delay)
        else:
            send_telegram_message(notif.recipient, notif.message_text, notif.delay)

        # Создаём запись в логе
        log_entry = NotificationLog(
            notification_id=notif.id,
            status="SUCCESS",
            error_message=None
        )
        db.add(log_entry)
        db.commit()

    except Exception as e:
        # Логгируем в случае исключения
        log_entry = NotificationLog(
            notification_id=notification_id,
            status="FAILED",
            error_message=str(e)
        )
        db.add(log_entry)
        db.commit()
    finally:
        db.close()
