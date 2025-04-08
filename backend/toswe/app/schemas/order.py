# app/schemas/order.py
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .order_item import OrderItem, Optional

class OrderBase(BaseModel):
    user_id: int
    payment_method: str
    status: str
    total_amount: float

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None
    total_amount: Optional[float] = None

class Order(OrderBase):
    id_order: int
    date_order: datetime
    items: List[OrderItem] = []

    class Config:
        orm_mode = True