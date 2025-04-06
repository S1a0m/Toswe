# app/models/announcement.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.db import Base

class Announcement(Base):
    __tablename__ = "announcements"

    id_announcement = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    img_annonce = Column(String)
    link_details = Column(String)
    sent = Column(DateTime, default=datetime.utcnow)
