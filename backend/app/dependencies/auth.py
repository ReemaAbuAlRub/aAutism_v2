# backend/app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.security import UserToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    token_cls=UserToken()
    payload = token_cls.decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
        )
    return user_id
