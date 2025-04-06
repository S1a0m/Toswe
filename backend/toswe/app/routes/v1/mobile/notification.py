from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
import crud.notification as crud_notification
import schemas

router = APIRouter(prefix="/notifications", tags=["mobile - notifications"])

@router.get("/{user_id}", response_model=list[schemas.Notification])
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    return crud_notification.get_notifications_for_user(db, user_id)
