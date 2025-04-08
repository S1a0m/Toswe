# app/crud/message.py
from sqlalchemy.orm import Session
from app.models.message import Message
from app.schemas.message import MessageCreate

def create_message(db: Session, msg: MessageCreate):
    new_msg = Message(**msg.dict())
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

def get_messages(db: Session):
    return db.query(Message).order_by(Message.time_sent.desc()).all()

def get_message(db: Session, id_message: int):
    return db.query(Message).filter(Message.id_message == id_message).first()

def delete_message(db: Session, id_message: int):
    msg = get_message(db, id_message)
    if msg:
        db.delete(msg)
        db.commit()
    return msg
