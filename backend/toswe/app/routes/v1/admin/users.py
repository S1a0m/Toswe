from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.routes.deps.dependencies import get_db, require_admin
import app.crud.user as crud_user
import app.schemas.user

router = APIRouter(prefix="/admin/users", tags=["admin - users"])

@router.get("/", response_model=List[app.schemas.user.User])
def get_all_users(
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_user.get_users(db)

@router.get("/{user_id}", response_model=app.schemas.user.User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_user.get_user(db, user_id)

@router.delete("/{user_id}", response_model=app.schemas.user.User)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_admin)
):
    return crud_user.delete_user(db, user_id)