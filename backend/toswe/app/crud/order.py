# app/crud/order.py
from sqlalchemy.orm import Session
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate


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

def delete_all_orders(db: Session):
    deleted = db.query(Order).delete()
    db.commit()
    return {"deleted": deleted}

def get_active_cart(db: Session, user_id: int):
    return db.query(Order).filter_by(user_id=user_id, status="draft").first()

def create_cart(db: Session, user_id: int):
    new_cart = Order(user_id=user_id, status="draft", total_amount=0)
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart

def get_or_create_cart(db: Session, user_id: int):
    cart = get_active_cart(db, user_id)
    return cart if cart else create_cart(db, user_id)

def checkout_order(db: Session, user_id: int):
    order = db.query(Order).filter(Order.user_id == user_id, Order.status == "pending").first()
    if not order:
        return None
    order.status = "paid"  # ou "confirmed"
    db.commit()
    db.refresh(order)
    return order

def get_cart(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id, Order.status == "pending").first()
