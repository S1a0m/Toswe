# schemas/notification.py
from pydantic import BaseModel
from datetime import datetime
# from typing import Optional

class MessageBase(BaseModel):
    mail_or_number: str
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id_message: int
    time_sent: datetime

    class Config:
        orm_mode = True

