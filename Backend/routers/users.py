# Backend/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from database import get_session
from models import User
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


# Simple request/response schemas the frontend expects
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=dict)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    # check existing user
    q = select(User).where(User.email == data.email)
    res = await session.exec(q)
    if res.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        is_admin=False
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"message": "User registered"}


@router.post("/login", response_model=Token)
async def login(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    res = await session.exec(q)
    user = res.first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "is_admin": current_user.is_admin}
