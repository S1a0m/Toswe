from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.routes.deps.dependencies import get_db, get_current_user
from app.models.product import Product, ProductCategory
from app.schemas.product import ProductAll, ProductSchema
from app.services.ml_recommender import recommend_products_for_user


router = APIRouter(prefix="/user/products", tags=["user - products"])


@router.get("/", response_model=list[ProductAll])
def list_products(
    category: ProductCategory = Query(...),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user)  # Remis ici pour sécurité
):
    products = db.query(Product).filter(
        Product.category == category,
        Product.published == True
    ).all()
    return products

@router.get("/search", response_model=list[ProductAll])
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


@router.get("/recommendations", response_model=list[ProductAll])
def get_recommendations(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return recommend_products_for_user(db, user["id_user"])