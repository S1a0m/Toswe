from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db
import app.crud.announcement as crud_announcement
import app.schemas.announcement

router = APIRouter(prefix="/admin/announcements", tags=["admin - announcements"])

@router.post("/", response_model=app.schemas.announcement.Announcement)
def create_announcement(ann: app.schemas.announcement.AnnouncementCreate, db: Session = Depends(get_db)):
    return crud_announcement.create_announcement(db, ann)
