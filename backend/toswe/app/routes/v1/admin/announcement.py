from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
import crud.announcement as crud_announcement
import schemas

router = APIRouter(prefix="/admin/announcements", tags=["admin - announcements"])

@router.post("/", response_model=schemas.Announcement)
def create_announcement(ann: schemas.AnnouncementCreate, db: Session = Depends(get_db)):
    return crud_announcement.create_announcement(db, ann)
