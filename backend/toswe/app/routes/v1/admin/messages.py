# app/routes/v1/admin/message.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.message import Message
from app.routes.deps.dependencies import get_db, require_admin
import app.crud.message as crud_message

router = APIRouter(prefix="/admin/messages", tags=["admin - messages"])

@router.get("/", response_model=List[Message])
def list_messages(db: Session = Depends(get_db), user: dict = Depends(require_admin)):
    return crud_message.get_messages(db)

@router.get("/{id_message}", response_model=Message)
def get_message(id_message: int, db: Session = Depends(get_db), user: dict = Depends(require_admin)):
    msg = crud_message.get_message(db, id_message)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg

@router.delete("/{id_message}", response_model=Message)
def delete_message(id_message: int, db: Session = Depends(get_db), user: dict = Depends(require_admin)):
    msg = crud_message.delete_message(db, id_message)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg
