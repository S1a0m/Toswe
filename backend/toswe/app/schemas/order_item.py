# app/schemas/order_item.py
from pydantic import BaseModel
from typing import Optional

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

class OrderItem(OrderItemBase):
    id_order_item: int

    class Config:
        orm_mode = True