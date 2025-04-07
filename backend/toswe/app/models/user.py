# app/models/user.py
from sqlalchemy import Column, Integer, String, Enum, Boolean
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
    # password