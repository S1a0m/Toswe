from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db, get_current_user
import app.crud.notification as crud_notification
import app.schemas.notification as schema_notification

router = APIRouter(prefix="/user/notifications", tags=["user - notifications"])

@router.get("/", response_model=list[schema_notification.Notification])
def get_my_notifications(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_notification.get_user_notifications(db, user["id_user"])
