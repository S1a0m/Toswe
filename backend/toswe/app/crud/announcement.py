from sqlalchemy.orm import Session
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate


def create_announcement(db: Session, annonce: AnnouncementCreate):
    db_annonce = Announcement(**annonce.dict())
    db.add(db_annonce)
    db.commit()
    db.refresh(db_annonce)
    return db_annonce


def get_announcement(db: Session, announcement_id: int):
    return db.query(Announcement).filter(Announcement.id_announcement == announcement_id).first()


def get_announcements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Announcement).offset(skip).limit(limit).all()


def update_announcement(db: Session, announcement_id: int, updated: AnnouncementUpdate):
    annonce = get_announcement(db, announcement_id)
    if annonce:
        for key, value in updated.dict(exclude_unset=True).items():
            setattr(annonce, key, value)
        db.commit()
        db.refresh(annonce)
    return annonce


def delete_announcement(db: Session, announcement_id: int):
    annonce = get_announcement(db, announcement_id)
    if annonce:
        db.delete(annonce)
        db.commit()
    return annonce

def delete_all_announcements(db: Session):
    deleted = db.query(Announcement).delete()
    db.commit()
    return {"deleted": deleted}
