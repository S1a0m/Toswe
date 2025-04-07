from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(**user.dict(exclude={"password"}), hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id_user == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, updated_user: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in updated_user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def delete_all_users(db: Session):
    deleted = db.query(User).delete()
    db.commit()
    return {"deleted": deleted}

def authenticate_user(db: Session, telephone: str, password: str):
    user = db.query(User).filter(User.telephone == telephone).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
