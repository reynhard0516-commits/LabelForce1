# Backend/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from models import User
from auth import hash_password, verify_password, create_access_token
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

# Pydantic input models
class UserCreate(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# dependency
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/register", response_model=dict)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    existing = (await session.exec(q)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"message": "User registered"}

@router.post("/login", response_model=TokenResponse)
async def login(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    user = (await session.exec(q)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

# helper to fetch current user from token
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    q = select(User).where(User.id == int(sub))
    user = (await session.exec(q)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/me")
async def read_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "is_admin": current_user.is_admin, "id": current_user.id}
