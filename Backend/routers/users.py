from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from Backend.models import User
from Backend.schemas import UserCreate, Token
from Backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from Backend.database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    result = await session.execute(q)

    if result.first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"message": "User registered"}


@router.post("/login", response_model=Token)
async def login(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    result = await session.execute(q)
    user = result.scalar()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def current_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "is_admin": current_user.is_admin}
