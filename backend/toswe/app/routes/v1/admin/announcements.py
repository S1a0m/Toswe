from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.routes.deps.dependencies import get_db, require_admin
import app.crud.announcement as crud_announcement
import app.schemas.announcement

router = APIRouter(prefix="/admin/announcements", tags=["admin - announcements"])


@router.post("/", response_model=app.schemas.announcement.Announcement)
def create_announcement(
    ann: app.schemas.announcement.AnnouncementCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_announcement.create_announcement(db, ann)


@router.delete("/", response_model=dict)
def delete_all_announcements(
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_announcement.delete_all_announcements(db)


@router.delete("/{id_announcement}", response_model=app.schemas.announcement.Announcement)
def delete_announcement(
    id_announcement: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_announcement.delete_announcement(db, id_announcement)


@router.get("/{id_announcement}", response_model=app.schemas.announcement.Announcement)
def get_announcement(
    id_announcement: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_announcement.get_announcement(db, id_announcement)


@router.get("/", response_model=List[app.schemas.announcement.Announcement])
def get_all_announcements(
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_announcement.get_announcements(db)


@router.put("/{id_announcement}", response_model=app.schemas.announcement.Announcement)
def update_announcement(
    id_announcement: int,
    updated_data: app.schemas.announcement.AnnouncementCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_announcement.update_announcement(db, id_announcement, updated_data)
