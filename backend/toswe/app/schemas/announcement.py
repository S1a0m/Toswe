# schemas/announcement.py
from pydantic import BaseModel
from datetime import datetime

class AnnouncementBase(BaseModel):
    description: str
    img_annonce: str
    link_details: str

class AnnouncementCreate(AnnouncementBase):
    pass

class Announcement(AnnouncementBase):
    id_announcement: int
    sent: datetime

    class Config:
        orm_mode = True