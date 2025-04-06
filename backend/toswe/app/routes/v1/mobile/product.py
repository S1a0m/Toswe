from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
import crud.product as crud_product
import schemas

router = APIRouter(prefix="/products", tags=["mobile - products"])

@router.get("/", response_model=list[schemas.Product])
def list_published_products(db: Session = Depends(get_db)):
    return crud_product.get_published_products(db)
