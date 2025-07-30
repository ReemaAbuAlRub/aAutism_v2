from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserCreate(BaseModel):
    email: EmailStr
    password: str= Field(min_length=8)


class UserRead(BaseModel):
    id: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
