import uuid
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import  HTTPException,status
from ..core.security import UserToken
from app.db.models.user import User
from app.schemas.user import UserCreate, UserRead, Token


class UserService:
    def __init__(self,db: Session):
        self.db = db
    
    def create_user(self, user_in: UserCreate) -> UserRead:
        existing = self.db.query(User).filter(User.email == user_in.email).first()
        if existing:
            raise ValueError(f"Email '{user_in.email}' is already registered")
        token_cls=UserToken()
        user = User(
            id=uuid.uuid4(),
            email=user_in.email,
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            autism_level=user_in.autism_level,
            password=token_cls.get_password_hash(user_in.password)
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return UserRead(id=str(user.id), email=user.email)

   
    def authenticate_user(self, email: str, password: str)-> Optional[Token]:
        user=self.db.query(User).filter(User.email==email).first()
        user_token=UserToken()

        if not user or not user_token.verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        print({"sub": str(user.id)})
        access_token=user_token.create_access_token({"sub": str(user.id)})

        return Token(access_token=access_token)

    
    def delete_user():
        pass