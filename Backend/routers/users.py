# Backend/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Any

from .. import models, schemas
from ..database import get_session
from ..auth import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=dict)
async def register(data: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    # check if user exists
    q = select(models.User).where(models.User.email == data.email)
    res = await session.exec(q)
    if res.first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(email=data.email, hashed_password=get_password_hash(data.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"message": "User registered"}


@router.post("/login", response_model=schemas.Token)
async def login(data: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    q = select(models.User).where(models.User.email == data.email)
    res = await session.exec(q)
    user = res.first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}


# helper to get current user (optional)
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from ..schemas import TokenData
from fastapi import Request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> models.User:
    from ..auth import SECRET_KEY, ALGORITHM
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    q = select(models.User).where(models.User.email == email)
    res = await session.exec(q)
    user = res.first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me")
async def me(current_user: models.User = Depends(get_current_user)):
    return {"email": current_user.email, "is_admin": current_user.is_admin}
