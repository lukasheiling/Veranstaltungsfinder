from pydantic import BaseModel
from typing import Optional, List

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
        
class EventBase(BaseModel):
    name: str
    date: str  # Format YYYY-MM-DD
    venue: str
    country: str
    url: Optional[str] = None  # Optional, um None-Werte zu unterstützen

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    class Config:
        orm_mode = True

class UserAuthenticate(BaseModel):
    email: str
    password: str
