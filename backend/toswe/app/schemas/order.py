# schemas/order.py
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .order_item import OrderItem

class OrderBase(BaseModel):
    user_id: int
    payment_method: str
    status: str
    total_amount: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id_order: int
    date_order: datetime
    items: List[OrderItem] = []

    class Config:
        orm_mode = True