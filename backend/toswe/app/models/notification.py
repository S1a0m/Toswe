# app/models/notification.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Notification(Base):
    __tablename__ = "notifications"

    id_notification = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    title = Column(String)
    description = Column(String)
    link_details = Column(String)
    time_sent = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)
    sent = Column(Boolean, default=False)

    user = relationship("User")
