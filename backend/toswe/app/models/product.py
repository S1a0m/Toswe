# app/models/product.py
from sqlalchemy import Column, Integer, String, Enum, Float, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from app.core.db import Base
import enum

class ProductCategory(str, enum.Enum):
    tech = "tech"
    local = "local"

class Product(Base):
    __tablename__ = "products"

    id_product = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(ProductCategory), default=ProductCategory.local)
    price = Column(Float, nullable=False)
    description = Column(ARRAY(String))
    images_list = Column(ARRAY(String))
    in_stock = Column(Boolean, default=True)
    published = Column(Boolean, default=False)
