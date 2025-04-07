from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db
import app.crud.order as crud_order
import app.schemas.order

router = APIRouter(prefix="/orders", tags=["mobile - orders"])

@router.post("/", response_model=app.schemas.order.Order)
def create_order(order: app.schemas.order.OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create_order(db, order)
