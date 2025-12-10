from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
from jose import jwt

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password: str) -> str:
    # returns a bcrypt hash
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.utcnow()
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "iat": int(now.timestamp()), "exp": int((now + expires_delta).timestamp())}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
