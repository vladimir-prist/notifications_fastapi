from pydantic import BaseModel, Field
from typing import Union, List


class NotificationIn(BaseModel):
    """ Схема входных данных при POST /api/notify. """
    message_text: str
    recipient: Union[str, List[str]]  # Один получатель или список
    delay: int = Field(..., ge=0, le=2)


class NotificationOut(BaseModel):
    """ Схема данных, которые возвращаются в ответ. """
    id: int
    message_text: str
    recipient: str
    delay: int

    class Config:
        orm_mode = True  # Позволяет Pydantic преобразовывать ORM-объекты в схемы
