from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.routes.deps.dependencies import get_db, require_admin
import app.crud.notification as crud_notification
import app.schemas.notification

router = APIRouter(prefix="/admin/notifications", tags=["admin - notifications"])

@router.post("/", response_model=app.schemas.notification.Notification)
def create_notification(
    notif: app.schemas.notification.NotificationCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_notification.create_notification(db, notif)

@router.get("/", response_model=List[app.schemas.notification.Notification])
def get_all_notifications(
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_notification.get_notifications(db)

@router.get("/{id_notification}", response_model=app.schemas.notification.Notification)
def get_notification(
    id_notification: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_notification.get_notification(db, id_notification)

@router.delete("/{id_notification}", response_model=app.schemas.notification.Notification)
def delete_notification(
    id_notification: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_notification.delete_notification(db, id_notification)