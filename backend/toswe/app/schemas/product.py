# schemas/product.py
from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    price: float
    description: Optional[str] = None
    images: Optional[List[str]] = []
    in_stock: Optional[bool] = True
    status: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    images: Optional[List[str]] = []
    in_stock: Optional[bool] = True
    status: Optional[str] = None

class ProductSchema(ProductBase):
    id_product: int

    class Config:
        orm_mode = True

class ProductAll(BaseModel):
    id_product: int
    name: str
    price: float
    image: str
    in_stock: bool
    status: str

    class Config:
        orm_mode = True