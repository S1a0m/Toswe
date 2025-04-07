from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db, get_current_user
import app.crud.announcement as crud_announcement
import app.schemas.announcement as schema_announcement

router = APIRouter(prefix="/user/announcements", tags=["user - announcements"])

@router.get("/", response_model=list[schema_announcement.Announcement])
def get_all_announcements(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return crud_announcement.get_announcements(db)

@router.get("/{id_announcement}", response_model=schema_announcement.Announcement)
def get_announcement(id_announcement: int, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return crud_announcement.get_announcement(db, id_announcement)
