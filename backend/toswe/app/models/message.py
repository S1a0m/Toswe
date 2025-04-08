# app/models/notification.py
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
# from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Message(Base):
    __tablename__ = "messages"

    id_message = Column(Integer, primary_key=True, index=True)
    mail_or_number = Column(String)
    content = Column(String)
    time_sent = Column(DateTime, default=datetime.utcnow)

