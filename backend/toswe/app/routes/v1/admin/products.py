from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from app.routes.deps.dependencies import get_db, require_admin
from app.models.product import Product
from app.schemas.product import Product as ProductSchema
import app.crud.product as crud_product
import app.schemas.product

router = APIRouter(prefix="/admin/products", tags=["admin - products"])

@router.post("/", response_model=app.schemas.product.Product)
def create_product(
    product: app.schemas.product.ProductCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_product.create_product(db, product)

@router.get("/", response_model=List[app.schemas.product.Product])
def get_all_products(
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_product.get_products(db)

@router.get("/{product_id}", response_model=app.schemas.product.Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_product.get_product(db, product_id)

@router.put("/{product_id}", response_model=app.schemas.product.Product)
def update_product(
    product_id: int,
    product_data: app.schemas.product.ProductCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_product.update_product(db, product_id, product_data)

@router.delete("/{product_id}", response_model=app.schemas.product.Product)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_product.delete_product(db, product_id)


@router.get("/search", response_model=list[ProductSchema])
def search_products(
    keyword: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    results = db.query(Product).filter(
        or_(
            Product.name.ilike(f"%{keyword}%"),
            Product.description.ilike(f"%{keyword}%")
        )
    ).all()
    return results