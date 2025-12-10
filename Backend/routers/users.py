from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from Backend.schemas import UserCreate, Token
from Backend.models import User
from Backend.database import get_session
from Backend.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    res = await session.execute(q)

    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password)
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"message": "User registered"}

@router.post("/login", response_model=Token)
async def login(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    res = await session.execute(q)
    user = res.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "is_admin": current_user.is_admin,
        "created_at": str(current_user.created_at)
    }
