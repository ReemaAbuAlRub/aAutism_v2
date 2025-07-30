from datetime import datetime, timedelta
from typing import Any, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

class UserToken:
    def __init__(self):
        self.pwd_context  = CryptContext(
                schemes=["bcrypt", "pbkdf2_sha256"],
                default="pbkdf2_sha256",
                deprecated="auto",
            )
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)


    def create_access_token(self, data: Dict[str, Any],expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta
            if expires_delta is not None
            else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
        return encoded_jwt


    def decode_access_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return {}
