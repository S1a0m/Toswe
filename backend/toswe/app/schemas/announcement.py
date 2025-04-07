from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnnouncementBase(BaseModel):
    description: str
    img_annonce: str
    link_details: str


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(BaseModel):
    description: Optional[str] = None
    img_annonce: Optional[str] = None
    link_details: Optional[str] = None


class Announcement(AnnouncementBase):
    id_announcement: int
    sent: datetime

    class Config:
        orm_mode = True
