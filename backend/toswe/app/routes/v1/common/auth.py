from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db, get_current_user
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.crud import user as crud_user
from app.schemas.token import Token, TokenRefresh, LoginInput
from app.services.auth_service import register_user, request_password_reset, reset_password
from app.schemas.user import UserCreate
# from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(login_data: LoginInput, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, login_data.mobile_number, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Numéro ou mot de passe incorrect")

    token_data = {"sub": str(user.id_user), "role": user.status}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
def refresh_token(token_data: TokenRefresh):
    payload = decode_token(token_data.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_access_token({"sub": payload["sub"], "role": payload["role"]})
    new_refresh = create_refresh_token({"sub": payload["sub"], "role": payload["role"]})

    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}

@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user_data)

@router.post("/request-password-reset")
def request_reset(data: dict, db: Session = Depends(get_db)):
    return request_password_reset(db, data["phone"])

@router.post("/reset-password")
def reset_password(data: dict, db: Session = Depends(get_db)):
    return reset_password(db, data["phone"], data["code"], data["new_password"])
