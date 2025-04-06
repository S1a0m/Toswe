from sqlalchemy.orm import Session
from models.order import Order
from schemas.order import OrderCreate, OrderUpdate


def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id_order == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Order).offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, updated: OrderUpdate):
    order = get_order(db, order_id)
    if order:
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(order, key, value)
        db.commit()
        db.refresh(order)
    return order


def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if order:
        db.delete(order)
        db.commit()
    return order
