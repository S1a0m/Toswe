# app/models/user.py
from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, DateTime, Float
import datetime
from app.core.db import Base
import enum

class UserStatus(str, enum.Enum):
    customer = "customer"
    seller = "seller"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id_user = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.customer)
    mobile_number = Column(String)
    address = Column(String)
    online = Column(Boolean, default=False)
    password = Column(String)

class UserHistory(Base):
    __tablename__ = "user_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id_user"))
    product_id = Column(Integer, ForeignKey("product.id"))
    viewed_at = Column(DateTime, default=datetime.datetime.utcnow)
    time_spent = Column(Float, default=0.0)  # en secondes
    interaction_score = Column(Float, default=1.0)  # clic simple = 1.0, ajout panier = 2.0, achat = 3.0
