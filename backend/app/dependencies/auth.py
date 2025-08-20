# backend/app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.security import UserToken
from app.db.session import get_db
from app.db.models.user import User
from sqlalchemy.orm import Session
from typing import Any
from uuid import UUID

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

# def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)) -> User:
#     token_cls=UserToken()
#     payload = token_cls.decode_access_token(token)
#     user = db.query(User).get(payload["sub"])
#     if not user:
#         raise HTTPException(401, "Unauthorized")
#     return user

def _coerce_sub_to_pk_type(sub: str) -> Any:
    """Coerce JWT 'sub' string to the Python type of User PK (int/UUID/str)."""
    if sub is None or sub == "":
        raise HTTPException(status_code=401, detail="Invalid token subject")

    try:
        pk_col = sa_inspect(User).primary_key[0]
        pytype = pk_col.type.python_type  # e.g., int or uuid.UUID or str
    except Exception:
        # Fallback: assume string PK
        pytype = str

    if pytype is int:
        try:
            return int(sub)
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token subject (expected int)")

    if pytype is UUID:
        try:
            return UUID(sub)
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token subject (expected UUID)")

    # Default (string PK)
    return sub


# ---- current user dependency ----
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    token_cls=UserToken()
    payload = token_cls.decode_access_token(token)
    sub = payload.get("sub")
    user_pk = _coerce_sub_to_pk_type(sub)

    user = db.get(User, user_pk)
    if not user or not getattr(user, "is_active", True):
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user