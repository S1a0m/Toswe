from fastapi import APIRouter, UploadFile, File, Form, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

import shutil
import os

from app.routes.deps.dependencies import get_db, require_admin
from app.models.product import Product, ProductCategory
from app.schemas.product import ProductAll, ProductSchema
import app.crud.product as crud_product
import app.schemas.product

router = APIRouter(prefix="/admin/products", tags=["admin - products"])

UPLOAD_DIR = "static/uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=app.schemas.product.ProductSchema)
def create_product(
    name: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    price: str = Form(...),
    images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    image_paths = []

    for img in images:
        filename = f"{name}_{img.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        image_paths.append(file_path)

    db_product = Product(
        name=name,
        category=category,
        description=description,
        price=price,
        status=status,
        images=image_paths  
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductAll])
def list_products(
    category: ProductCategory = Query(...),
    db: Session = Depends(get_db),
    _: dict = Depends(require_admin)
):
    if category != 'all':
        products = db.query(Product).filter(
        Product.category == category,
            # Product.published == True
        ).all()
    else:
        products = db.query(Product)

    # On transforme les produits pour ne garder que la première image
    result = [
        ProductAll(
            id_product=product.id_product,
            name=product.name,
            status=product.status,
            price=product.price,
            image=product.images[0] if product.images else None,
            in_stock=product.in_stock
        )
        for product in products
    ]

    return result

@router.get("/{product_id}", response_model=app.schemas.product.ProductSchema)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_product.get_product(db, product_id)

@router.put("/{product_id}", response_model=app.schemas.product.ProductSchema)
def update_product(
    product_id: int,
    product_data: app.schemas.product.ProductCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_product.update_product(db, product_id, product_data)

@router.delete("/{product_id}", response_model=app.schemas.product.ProductSchema)
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