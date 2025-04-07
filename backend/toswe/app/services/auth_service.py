from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, get_password_hash

def register_user(db: Session, user_data):
    # Vérifier si déjà existant
    if db.query(User).filter_by(telephone=user_data.telephone).first():
        raise HTTPException(400, detail="Utilisateur existe déjà")
    
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(**user_data.dict(), password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def change_password(db: Session, user_id: int, old_pw: str, new_pw: str):
    user = db.query(User).filter_by(id_user=user_id).first()
    if not user or not verify_password(old_pw, user.password):
        raise HTTPException(403, detail="Ancien mot de passe invalide")

    user.password = get_password_hash(new_pw)
    db.commit()
    return {"msg": "Mot de passe changé avec succès"}
