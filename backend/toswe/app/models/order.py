# app/models/order.py
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base

class Order(Base):
    __tablename__ = "orders"

    id_order = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id_user"), nullable=False)
    date_order = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String)
    status = Column(String)
    total_amount = Column(Float)

    user = relationship("User")
    items = relationship("OrderItem", back_populates="order")
