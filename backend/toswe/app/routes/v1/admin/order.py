from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
import crud.order as crud_order
import schemas

router = APIRouter(prefix="/admin/orders", tags=["admin - orders"])

@router.get("/", response_model=list[schemas.Order])
def list_all_orders(db: Session = Depends(get_db)):
    return crud_order.get_all_orders(db)
