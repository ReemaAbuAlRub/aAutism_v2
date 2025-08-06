# backend/app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.security import UserToken
from app.db.session import get_db
from app.db.models.user import User
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

# def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
#     token_cls=UserToken()
#     payload = token_cls.decode_access_token(token)
#     user_id = payload.get("sub")
#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired authentication token",
#         )
#     return user_id

def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)) -> User:
    token_cls=UserToken()
    payload = token_cls.decode_access_token(token)
    user = db.query(User).get(payload["sub"])
    if not user:
        raise HTTPException(401, "Unauthorized")
    return user
