from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_session
from models import User
from auth import (
    verify_password,
    create_access_token,
    get_password_hash,
    decode_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# =====================================================
# SCHEMAS
# =====================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


# =====================================================
# AUTH ROUTES (PUBLIC)
# =====================================================

@router.post("/login")
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.email == data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 🔐 JWT now includes ROLE
    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


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
        password=hashed_password,
        role="user"  # 👈 default role
    )

    session.add(user)
    await session.commit()

    return {"message": "User created successfully"}


# =====================================================
# AUTHENTICATED ROUTES (JWT REQUIRED)
# =====================================================

@router.get("/me")
async def get_me(
    token=Depends(decode_token),
    session: AsyncSession = Depends(get_session)
):
    email = token.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await session.execute(
        select(User).where(User.email == email)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }


@router.get("/protected")
async def protected_route(token=Depends(decode_token)):
    return {
        "message": "You are authorized",
        "user": token["sub"],
        "role": token["role"]
    }


# =====================================================
# ADMIN-ONLY ROUTE
# =====================================================

@router.get("/admin")
async def admin_only(token=Depends(decode_token)):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return {
        "message": "Welcome admin",
        "user": token["sub"]
    }
