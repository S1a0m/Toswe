from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.routes.deps.dependencies import get_db
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.crud import user as crud_user
from app.schemas.token import Token, TokenRefresh, LoginInput
from services.auth_service import register_user, change_password
# from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(login_data: LoginInput, db: Session = Depends(get_db)):
    user = crud_user.authenticate_user(db, login_data.telephone, login_data.password)
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
def register(user_data: RegisterSchema, db: Session = Depends(get_db)):
    return register_user(db, user_data)

@router.post("/change-password")
def change(user_pw: ChangePasswordSchema, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return change_password(db, user["id_user"], user_pw.old_password, user_pw.new_password)
