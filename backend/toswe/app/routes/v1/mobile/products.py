from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.routes.deps.dependencies import get_db, get_current_user
from app.models import Product
from app.schemas.product import Product as ProductSchema
from app.services.ml_recommender import recommend_products_for_user


router = APIRouter(prefix="/user/products", tags=["user - products"])

@router.get("/", response_model=list[ProductSchema])
def list_all_products(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return db.query(Product).all()

@router.get("/search", response_model=list[ProductSchema])
def search_products(keyword: str = Query(..., min_length=1), db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return db.query(Product).filter(
        or_(
            Product.name.ilike(f"%{keyword}%"),
            Product.description.ilike(f"%{keyword}%")
        )
    ).all()

@router.get("/{id_product}", response_model=ProductSchema)
def get_product(id_product: int, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return db.query(Product).filter(Product.id_product == id_product).first()


@router.get("/recommendations", response_model=list[Product])
def get_recommendations(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return recommend_products_for_user(db, user["id_user"])