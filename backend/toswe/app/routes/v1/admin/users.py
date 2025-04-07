from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db
import app.crud.user as crud_user
import app.schemas.user

router = APIRouter(prefix="/admin/users", tags=["admin - users"])

@router.get("/", response_model=list[app.schemas.user.User])
def get_all_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users(db)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud_user.delete_user(db, user_id)
