from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db
import app.crud.product as crud_product
import app.schemas.product

router = APIRouter(prefix="/products", tags=["mobile - products"])

@router.get("/", response_model=list[app.schemas.product.Product])
def list_published_products(db: Session = Depends(get_db)):
    return crud_product.get_published_products(db)
