# schemas/notification.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationBase(BaseModel):
    user_id: int
    title: str
    description: str
    link_details: str
    read: bool = False
    sent: bool = False

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    user_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    link_details: Optional[str] = None
    read: bool = False
    sent: bool = False

class Notification(NotificationBase):
    id_notification: int
    time_sent: datetime

    class Config:
        orm_mode = True