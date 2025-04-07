# schemas/user.py
from pydantic import BaseModel
from enum import Enum
from typing import Optional

class UserStatus(str, Enum):
    customer = "customer"
    seller = "seller"
    admin = "admin"

class UserBase(BaseModel):
    name: str
    surname: str
    status: UserStatus = UserStatus.customer
    mobile_number: str
    address: str
    online: bool = False

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    status: UserStatus = UserStatus.customer
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    online: bool = False

class User(UserBase):
    id_user: int

    class Config:
        orm_mode = True