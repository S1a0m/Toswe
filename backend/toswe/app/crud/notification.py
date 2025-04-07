from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate


def create_notification(db: Session, notif: NotificationCreate):
    db_notif = Notification(**notif.dict())
    db.add(db_notif)
    db.commit()
    db.refresh(db_notif)
    return db_notif


def get_notification(db: Session, notification_id: int):
    return db.query(Notification).filter(Notification.id_notification == notification_id).first()


def get_notifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Notification).offset(skip).limit(limit).all()


def update_notification(db: Session, notification_id: int, updated: NotificationUpdate):
    notif = get_notification(db, notification_id)
    if notif:
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(notif, key, value)
        db.commit()
        db.refresh(notif)
    return notif


def delete_notification(db: Session, notification_id: int):
    notif = get_notification(db, notification_id)
    if notif:
        db.delete(notif)
        db.commit()
    return notif

def delete_all_notifications(db: Session):
    deleted = db.query(Notification).delete()
    db.commit()
    return {"deleted": deleted}