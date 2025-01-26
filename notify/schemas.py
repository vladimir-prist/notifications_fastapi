from pydantic import BaseModel, Field, ConfigDict
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
    model_config = ConfigDict(str_max_length=10)
