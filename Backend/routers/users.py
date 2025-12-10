from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import User
from ..schemas import UserCreate, Token
from ..auth import hash_password, verify_password, create_access_token, get_current_user
from ..database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=dict)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    res = await session.execute(q)
    if res.first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"message": "User registered"}

@router.post("/login", response_model=Token)
async def login(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(User).where(User.email == data.email)
    res = await session.execute(q)
    user = res.scalar_one_or_none()

    if not
