# schemas/notification.py
from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    user_id: int
    title: str
    description: str
    link_details: str
    read: bool = False
    sent: bool = False

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id_notification: int
    time_sent: datetime

    class Config:
        orm_mode = True