# nehanda_app.py
import os
import jwt
from datetime import datetime
from typing import Optional, List

# --- FastAPI / Pydantic ---
from fastapi import FastAPI, Depends, HTTPException, status, Header
from pydantic import BaseModel

# --- SQLAlchemy (db des conversations, distincte de Django) ---
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session

# --- Django ORM (pour User & settings) ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "toswe.settings"))
import django  # type: ignore
django.setup()
from django.conf import settings
from users.models import User  # ton modèle User existant côté Django

# ============ SQLAlchemy setup (DB conversations) ============
CONV_DB_URL = os.getenv("CONVERSATIONS_DB_URL", "sqlite:///./conversations.db")
engine = create_engine(CONV_DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String(20), nullable=False)  # "user" | "nehanda"
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

Base.metadata.create_all(bind=engine)

# ============ FastAPI schemas ============
class ChatIn(BaseModel):
    message: str
    conversation_id: Optional[int] = None  # si non fourni, on (re)prend la conv active ou on crée

class ChatOut(BaseModel):
    conversation_id: int
    response: str

class MessageOut(BaseModel):
    id: int
    sender: str
    text: str
    created_at: datetime

class ConversationOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    messages: List[MessageOut]

# ============ Dependencies ============
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """
    Attend un header: Authorization: Bearer <token>
    Le token est le JWT que tu émets côté Django (HS256, SECRET_KEY).
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    racine_id = payload.get("racine_id")
    if not racine_id:
        raise HTTPException(status_code=401, detail="Invalid payload")

    try:
        user = User.objects.get(racine_id=racine_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ============ “Cerveau” minimal de Nehanda (stub) ============
def nehada_brain_reply(user: User, message: str) -> str:
    # TODO: remplace par ton vrai moteur (règles, RAG, TF, etc.)
    return f"Je t’ai bien lu, {getattr(user, 'username', user.pk)} : “{message}”. Que souhaites-tu acheter ?"

# ============ FastAPI app ============
app = FastAPI(title="Nehanda", version="0.1.0")

@app.post("/chat", response_model=ChatOut)
def chat_with_nehanda(payload: ChatIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # 1) Récupération/Création de la conversation
    conv: Optional[Conversation] = None
    if payload.conversation_id:
        conv = db.get(Conversation, payload.conversation_id)
        if not conv or conv.user_id != user.id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        # Reprendre la plus récente conversation existante (optionnel)…
        conv = db.query(Conversation).filter(Conversation.user_id == user.id).order_by(Conversation.id.desc()).first()
        if conv is None:
            conv = Conversation(user_id=user.id)
            db.add(conv)
            db.flush()  # obtient conv.id

    # 2) Sauvegarder le message utilisateur
    db.add(Message(conversation_id=conv.id, sender="user", text=payload.message))

    # 3) Générer la réponse de Nehanda
    reply = nehada_brain_reply(user, payload.message)

    # 4) Sauvegarder la réponse
    db.add(Message(conversation_id=conv.id, sender="nehanda", text=reply))
    db.commit()

    return ChatOut(conversation_id=conv.id, response=reply)

@app.get("/conversations/{conversation_id}", response_model=ConversationOut)
def get_conversation(conversation_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    conv = db.get(Conversation, conversation_id)
    if not conv or conv.user_id != user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Charger messages pour la réponse Pydantic
    msgs = (
        db.query(Message)
        .filter(Message.conversation_id == conv.id)
        .order_by(Message.id.asc())
        .all()
    )

    return ConversationOut(
        id=conv.id,
        user_id=conv.user_id,
        created_at=conv.created_at,
        messages=[MessageOut(id=m.id, sender=m.sender, text=m.text, created_at=m.created_at) for m in msgs],
    )
