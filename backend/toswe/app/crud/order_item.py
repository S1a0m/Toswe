# app/crud/order_item.py

from app.crud.order import get_cart, create_order
from app.schemas.order import OrderCreate
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime


def create_order_item(db: Session, item: OrderItemCreate, user_id: int):
    # Vérifier si un panier existe
    order = get_cart(db, user_id)
    
    # S'il n'existe pas, on en crée un
    if not order:
        order_create = OrderCreate(
            user_id=user_id,
            payment_method="not_set",
            status="pending",
            total_amount=0.0
        )
        order = create_order(db, order_create)

    # Créer l'article de commande
    db_item = OrderItem(
        order_id=order.id_order,
        product_id=item.product_id,
        quantity=item.quantity,
        unit_price=item.unit_price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    # Mettre à jour le total
    update_order_total(db, order.id_order)
    return db_item



def get_order_item(db: Session, item_id: int):
    return db.query(OrderItem).filter(OrderItem.id_order_item == item_id).first()


def get_order_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(OrderItem).offset(skip).limit(limit).all()


def update_order_item(db: Session, item_id: int, updated: OrderItemUpdate):
    item = get_order_item(db, item_id)
    if item:
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        update_order_total(db, item.order_id)
    return item



def delete_order_item(db: Session, item_id: int):
    item = get_order_item(db, item_id)
    if item:
        order_id = item.order_id
        db.delete(item)
        db.commit()
        update_order_total(db, order_id)
    return item


def add_product_to_cart(db: Session, cart_id: int, product_id: int, quantity: int, unit_price: float):
    existing_item = db.query(OrderItem).filter_by(order_id=cart_id, product_id=product_id).first()

    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = OrderItem(order_id=cart_id, product_id=product_id, quantity=quantity, unit_price=unit_price)
        db.add(new_item)

    db.commit()

def delete_item_from_cart(db: Session, user_id: int, item_id: int):
    item = db.query(OrderItem).join(Order).filter(
        OrderItem.id_order_item == item_id,
        Order.user_id == user_id,
        Order.status == "pending"
    ).first()

    if not item:
        return None

    db.delete(item)
    db.commit()
    update_order_total(db, item.order_id)
    return item

def update_order_total(db: Session, order_id: int):
    total = db.query(func.sum(OrderItem.unit_price * OrderItem.quantity)) \
              .filter(OrderItem.order_id == order_id).scalar() or 0.0
    order = db.query(Order).filter(Order.id_order == order_id).first()
    if order:
        order.total_amount = total
        db.commit()
        db.refresh(order)
