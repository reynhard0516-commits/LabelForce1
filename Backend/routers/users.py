from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from database import get_session
from models import User
from auth import (
    verify_password,
    create_access_token,
    get_password_hash
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# -----------------------
# LOGIN
# -----------------------
@router.post("/login")
async def login(
    email: str,
    password: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# -----------------------
# REGISTER
# -----------------------
class RegisterRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(
    data: RegisterRequest,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.email == data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(data.password)

    user = User(
        email=data.email,
        password=hashed_password
    )

    session.add(user)
    await session.commit()

    return {"message": "User created successfully"}

# -----------------------
# HEALTH CHECK
# -----------------------
@router.get("/ping")
def ping():
    return {"status": "ok"}
