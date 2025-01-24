from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Union, List
from notify import models, schemas
from notify.database import get_db
from notify.tasks import send_notification_task

router = APIRouter()


@router.post("/notify", response_model=Union[schemas.NotificationOut, List[schemas.NotificationOut]])
def notify(notification: schemas.NotificationIn, db: Session = Depends(get_db)):
    """
    Точка входа: POST /api/notify
    Принимаем message, recipient (строка или список), delay.
    """

    def delay_to_seconds(delay_code: int) -> int:
        """ Отложенная отправка: 0 - сейчас, 1 - через 1 час, 2 - через 24 часа. """
        if delay_code == 1:
            return 3600
        elif delay_code == 2:
            return 86400
        return 0

    created_notifications = []

    # Если пришёл список получателей - создаём по отдельной записи на каждого
    if isinstance(notification.recipient, list):
        for one_rcp in notification.recipient:
            new_notif = models.Notification(
                message_text=notification.message_text,
                recipient=one_rcp,
                delay=notification.delay
            )
            db.add(new_notif)
            db.commit()
            db.refresh(new_notif)

            # Планируем задачу в Celery с нужной задержкой:
            send_notification_task.apply_async(
                args=[new_notif.id],
                countdown=delay_to_seconds(notification.delay)
            )
            created_notifications.append(new_notif)
        return created_notifications
    else:
        # Если один получатель - аналогично, но одна запись
        new_notif = models.Notification(
            message_text=notification.message_text,
            recipient=notification.recipient,
            delay=notification.delay
        )
        db.add(new_notif)
        db.commit()
        db.refresh(new_notif)

        send_notification_task.apply_async(
            args=[new_notif.id],
            countdown=delay_to_seconds(notification.delay)
        )
        return new_notif
