from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union, List
from notify import models, schemas
from notify.database import get_db
from notify.tasks import send_notification_task
from notify.services import delay_to_seconds

router = APIRouter()


@router.post("/notify", response_model=Union[schemas.NotificationOut, List[schemas.NotificationOut]])
async def notify(notification: schemas.NotificationIn, db: AsyncSession = Depends(get_db)):
    """
    Точка входа: POST /api/notify
    Принимаем message, recipient (строка или список), delay.
    """
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
            await db.commit()
            await db.refresh(new_notif)

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
        await db.commit()
        await db.refresh(new_notif)

        send_notification_task.apply_async(
            args=[new_notif.id],
            countdown=delay_to_seconds(notification.delay)
        )
        return new_notif
