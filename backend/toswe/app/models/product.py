# app/models/product.py
from sqlalchemy import Column, Integer, String, Enum, Float, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from app.core.db import Base
import enum

class ProductCategory(str, enum.Enum):
    computer = "computer"
    local = "local"
    accessories = "accessories"
    fashion = "fashion"
    sport = "sport"
    art = "art"
    all = "all"

class ProductStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    unpublished = "unpublished"

class Product(Base):
    __tablename__ = "products"

    id_product = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(ProductCategory, native_enum=False), default=ProductCategory.local)
    status = Column(Enum(ProductStatus, native_enum=False), default=ProductStatus.draft)
    price = Column(Float, nullable=False)
    description = Column(String)
    images = Column(ARRAY(String))
    in_stock = Column(Boolean, default=True)
