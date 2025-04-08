# app/routes/v1/client/message.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.message import Message, MessageCreate
from app.routes.deps.dependencies import get_db
import app.crud.message as crud_message

router = APIRouter(prefix="/messages", tags=["client - messages"])

@router.post("/", response_model=Message)
def send_message(msg: MessageCreate, db: Session = Depends(get_db)):
    return crud_message.create_message(db, msg)
