from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
import crud.order as crud_order
import schemas

router = APIRouter(prefix="/orders", tags=["mobile - orders"])

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create_order(db, order)
