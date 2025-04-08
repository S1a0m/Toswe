# app/routes/mobile/orders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db, get_current_user
import app.crud.order as crud_order
import app.schemas.order as schema_order
import app.schemas.order_item as schema_order_item
import app.crud.order_item as crud_order_item 
from app.schemas.order_item import OrderItemCreate, OrderItem, OrderItemUpdate

router = APIRouter(prefix="/user/orders", tags=["user - orders"])

@router.post("/", response_model=schema_order.Order)
def create_order(order: schema_order.OrderCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_order.create_order(db, user["id_user"], order)

@router.get("/", response_model=list[schema_order.Order])
def get_my_orders(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_order.get_user_orders(db, user["id_user"])

@router.get("/{id_order}", response_model=schema_order.Order)
def get_order(id_order: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_order.get_user_order_by_id(db, user["id_user"], id_order)

@router.post("/checkout", response_model=schema_order.Order)
def checkout_order(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    order = crud_order.checkout_order(db, user["id_user"])
    if not order:
        raise HTTPException(status_code=404, detail="Panier introuvable")
    return order

@router.delete("/items/{item_id}", response_model=schema_order_item.OrderItem)
def delete_item(item_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    item = crud_order_item.delete_item_from_cart(db, user["id_user"], item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Article introuvable dans le panier")
    return item

@router.post("/items/", response_model=OrderItem)
def add_item_to_cart(
    item: OrderItemCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return crud_order_item.create_order_item(db, item, user["id_user"])

@router.delete("/items/{item_id}", response_model=schema_order_item.OrderItem)
def remove_item_from_cart(item_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_order_item.delete_order_item(db, item_id)

@router.put("/items/{item_id}", response_model=schema_order_item.OrderItem)
def update_cart_item(
    item_id: int,
    item_data: OrderItemUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    return crud_order_item.update_order_item(db, item_id, item_data)