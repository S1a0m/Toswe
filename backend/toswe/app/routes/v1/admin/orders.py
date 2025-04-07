from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db
import app.crud.order as crud_order
import app.schemas.order

router = APIRouter(prefix="/admin/orders", tags=["admin - orders"])

@router.get("/", response_model=list[app.schemas.order.Order])
def list_all_orders(db: Session = Depends(get_db)):
    return crud_order.get_all_orders(db)
