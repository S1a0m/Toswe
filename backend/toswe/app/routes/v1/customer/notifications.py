from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db
import app.crud.notification as crud_notification
import app.schemas.notification

router = APIRouter(prefix="/notifications", tags=["mobile - notifications"])

@router.get("/{user_id}", response_model=list[app.schemas.notification.Notification])
def get_user_notifications(user_id: int, db: Session = Depends(get_db)):
    return crud_notification.get_notifications_for_user(db, user_id)
