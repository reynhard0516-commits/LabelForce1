
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.config import settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd.hash(password)

def verify_password(password: str, hash: str):
    return pwd.verify(password, hash)

def create_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALG)
