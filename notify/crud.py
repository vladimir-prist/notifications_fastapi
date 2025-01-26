from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from notify.models import Notification, NotificationLog


async def get_notification_by_id(db: AsyncSession, notification_id: int) -> Notification | None:
    """ Асинхронно получаем Notification по id через SQLAlchemy Core или ORM. """
    stmt = select(Notification).where(Notification.id == notification_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_notification_log(
        db: AsyncSession,
        notification_id: int,
        status: str,
        error_message: str | None = None
) -> NotificationLog:
    """ Создаёт запись в таблице notification_logs. """
    log_entry = NotificationLog(
        notification_id=notification_id,
        status=status,
        error_message=error_message
    )
    db.add(log_entry)
    await db.commit()
    await db.refresh(log_entry)
    return log_entry
