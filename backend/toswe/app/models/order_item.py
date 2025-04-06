# app/models/order_item.py
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.db import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id_order_item = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id_order"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id_product"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
