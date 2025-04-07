from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db
import app.crud.notification as crud_notification
import app.schemas.notification

router = APIRouter(prefix="/admin/notifications", tags=["admin - notifications"])

@router.post("/", response_model=app.schemas.notification.Notification)
def create_notification(notification: app.schemas.notification.NotificationCreate, db: Session = Depends(get_db)):
    return crud_notification.create_notification(db, notification)
