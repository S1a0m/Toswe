# schemas/user.py
from pydantic import BaseModel
from enum import Enum

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

class User(UserBase):
    id_user: int

    class Config:
        orm_mode = True