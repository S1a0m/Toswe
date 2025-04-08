from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db, get_current_user
import app.crud.user as crud_user
import app.schemas.user as schema_user

router = APIRouter(prefix="/user/profile", tags=["user - profile"])

@router.get("/", response_model=schema_user.User)
def get_my_profile(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_user.get_user(db, user["id_user"])

@router.put("/", response_model=schema_user.User)
def update_my_profile(update_data: schema_user.UserUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_user.update_user(db, user["id_user"], update_data)

@router.delete("/", response_model=schema_user.User)
def delete_my_account(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return crud_user.delete_user(db, user["id_user"])
