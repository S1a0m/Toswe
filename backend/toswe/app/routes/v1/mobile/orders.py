from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db, get_current_user
import app.crud.order as crud_order
import app.schemas.order as schema_order

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
