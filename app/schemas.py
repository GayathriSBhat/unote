from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    password: str


class UserOut(BaseModel):
    user_id: str
    user_name: str
    user_email: EmailStr
    created_on: datetime
    last_update: datetime


class Config:
    orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class NoteCreate(BaseModel):
    note_title: Optional[str]
    note_content: Optional[str]


class NoteOut(BaseModel):
    note_id: str
    user_id: str
    note_title: Optional[str]
    note_content: Optional[str]
    created_on: datetime
    last_update: datetime


class Config:
    orm_mode = True