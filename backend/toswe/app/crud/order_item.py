from sqlalchemy.orm import Session
from models.order_item import OrderItem
from schemas.order_item import OrderItemCreate, OrderItemUpdate


def create_order_item(db: Session, item: OrderItemCreate):
    db_item = OrderItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
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
    return item


def delete_order_item(db: Session, item_id: int):
    item = get_order_item(db, item_id)
    if item:
        db.delete(item)
        db.commit()
    return item
