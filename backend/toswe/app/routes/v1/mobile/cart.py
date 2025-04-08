from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db, get_current_user
import app.crud.order as crud_order
import app.crud.order_item as crud_item
import app.schemas.order as schema_order

router = APIRouter(prefix="/user/cart", tags=["user - cart"])

@router.post("/add")
def add_to_cart(product_id: int, quantity: int, unit_price: float, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    cart = crud_order.get_or_create_cart(db, user["id_user"])
    crud_item.add_product_to_cart(db, cart.id_order, product_id, quantity, unit_price)
    return {"message": "Produit ajouté au panier"}

@router.get("/", response_model=schema_order.Order)
def get_my_cart(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    cart = crud_order.get_active_cart(db, user["id_user"])
    if not cart:
        raise HTTPException(404, detail="Panier vide")
    return cart

@router.get("/cart", response_model=schema_order.Order)
def get_cart(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    cart = crud_order.get_cart(db, user["id_user"])
    if not cart:
        raise HTTPException(status_code=404, detail="Panier vide ou inexistant")
    return cart
