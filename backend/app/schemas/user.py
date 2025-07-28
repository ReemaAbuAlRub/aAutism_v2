from pydantic import BaseModel, EmailStr, Field,Date

class UserCreate(BaseModel):
    email: EmailStr
    date_of_birth: Date
    password: str= Field(min_length=8)


class