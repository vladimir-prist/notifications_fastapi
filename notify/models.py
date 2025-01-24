from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from notify.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message_text = Column(String(1024), nullable=False)
    recipient = Column(String(150), nullable=False)  # Email или telegram-id
    delay = Column(Integer, nullable=False)
    notification_logs = relationship(
        "NotificationLog",
        back_populates="notification"
    )


class NotificationLog(Base):
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
    status = Column(String(50), nullable=False) # SUCCESS/FAILED
    error_message = Column(Text)
