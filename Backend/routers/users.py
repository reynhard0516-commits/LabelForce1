from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from database import get_session
from models import User
from schemas import UserCreate, Token
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=dict)
async def register(data: UserCreate, session=Depends(get_session)):
    query = select(User).where(User.email == data.email)
    res = await session.execute(query)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=data.email, hashed_password=hash_password(data.password))
    session.add(user)
    await session.commit()
    return {"message": "User registered"}

@router.post("/login", response_model=Token)
async def login(data: UserCreate, session=Depends(get_session)):
    query = select(User).where(User.email == data.email)
    res = await session.execute(query)
    user = res.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def me(user=Depends(get_current_user)):
    return {
        "email": user.email,
        "is_admin": user.is_admin
    }
