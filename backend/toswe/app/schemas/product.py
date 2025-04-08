# schemas/product.py
from pydantic import BaseModel
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    price: float
    description: Optional[str] = None
    images_list: Optional[List[str]] = []
    in_stock: Optional[bool] = True
    published: Optional[bool] = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    images_list: Optional[List[str]] = []
    in_stock: Optional[bool] = True
    published: Optional[bool] = False

class ProductSchema(ProductBase):
    id_product: int

    class Config:
        orm_mode = True

class ProductAll(BaseModel):
    id_product: int
    name: str
    price: float
    images_list: List[str]
    in_stock: bool

    class Config:
        orm_mode = True