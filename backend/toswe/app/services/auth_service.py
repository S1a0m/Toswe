from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password
from app.services.whatsapp import send_whatsapp_code
import random

def register_user(db: Session, user_data):
    # Vérifier si déjà existant
    if db.query(User).filter_by(mobile_number=user_data.mobile_number).first():
        raise HTTPException(status_code=400, detail="Utilisateur existe déjà")
    
    data = user_data.dict()
    data["password"] = hash_password(data["password"])
    
    new_user = User(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


reset_code_storage = {}

def request_password_reset(db: Session, phone: str):
    user = db.query(User).filter_by(mobile_number=phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="Numéro non enregistré")

    code = str(random.randint(100000, 999999))
    reset_code_storage[phone] = code

    send_whatsapp_code(phone, code)  # Doit être défini dans app/services/whatsapp.py
    return {"msg": "Code envoyé via WhatsApp"}

def reset_password(db: Session, phone: str, code: str, new_pw: str):
    saved_code = reset_code_storage.get(phone)
    if not saved_code or saved_code != code:
        raise HTTPException(status_code=403, detail="Code invalide")

    user = db.query(User).filter_by(mobile_number=phone).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    user.password = hash_password(new_pw)
    db.commit()

    # Supprimer le code utilisé
    reset_code_storage.pop(phone, None)
    return {"msg": "Mot de passe réinitialisé avec succès"}

# def change_password(db: Session, user_id: int, old_pw: str, new_pw: str):
    user = db.query(User).filter_by(id_user=user_id).first()
    if not user or not verify_password(old_pw, user.password):
        raise HTTPException(403, detail="Ancien mot de passe invalide")

    user.password = hash_password(new_pw)
    db.commit()
    return {"msg": "Mot de passe changé avec succès"}

