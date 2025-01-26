import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from notify.database import Base
from sqlalchemy.dialects.postgresql import ENUM as PgEnum


class Notification(Base):
    """ Модель уведомлений. """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message_text = Column(String(1024), nullable=False)
    recipient = Column(String(150), nullable=False)  # Email или telegram-id
    delay = Column(Integer, nullable=False)
    notification_logs = relationship(
        "NotificationLog",
        back_populates="notification"
    )


class EnumStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class NotificationLog(Base):
    """ Модель логирования. """

    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(
        Integer,
        ForeignKey('notifications.id'),
        nullable=False
    )
    notification = relationship(
        "Notification",
        back_populates="notification_logs"
    )
    status = Column(PgEnum(EnumStatus, name='enum_status', create_type=False), nullable=False)
    error_message = Column(Text)
