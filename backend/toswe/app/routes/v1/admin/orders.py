from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.routes.deps.dependencies import get_db, require_admin
import app.crud.order as crud_order
import app.schemas.order

router = APIRouter(prefix="/admin/orders", tags=["admin - orders"])

@router.get("/", response_model=List[app.schemas.order.Order])
def get_all_orders(
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_order.get_orders(db)

@router.get("/{order_id}", response_model=app.schemas.order.Order)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_order.get_order(db, order_id)

@router.delete("/{order_id}", response_model=app.schemas.order.Order)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_order.delete_order(db, order_id)