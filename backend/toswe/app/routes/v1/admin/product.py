from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
import crud.product as crud_product
import schemas

router = APIRouter(prefix="/admin/products", tags=["admin - products"])

@router.post("/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, product)

@router.put("/{product_id}")
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.update_product(db, product_id, product)

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud_product.delete_product(db, product_id)
