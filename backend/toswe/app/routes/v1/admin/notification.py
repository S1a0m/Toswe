from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
import crud.notification as crud_notification
import schemas

router = APIRouter(prefix="/admin/notifications", tags=["admin - notifications"])

@router.post("/", response_model=schemas.Notification)
def send_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    return crud_notification.send_notification(db, notification)
