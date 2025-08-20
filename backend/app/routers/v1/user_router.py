from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.user import *
from app.dependencies.auth import get_current_user
router=APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    svc = UserService(db)
    try:
        user=svc.create_user(user_in)
        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Failed to Create User")


@router.post("/login", response_model=Token)
def login( form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    svc = UserService(db)
    try:
        token=svc.authenticate_user(form_data.username,form_data.password) 
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return {
        "access_token": token.access_token,
        "token_type": token.token_type}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access") 

@router.get("/me")
def read_me(current_user: UserCreate = Depends(get_current_user)):
        return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": getattr(current_user, "first_name", None),
        "last_name": getattr(current_user, "last_name", None),
        "autism_level": getattr(current_user, "autism_level", None),

    }