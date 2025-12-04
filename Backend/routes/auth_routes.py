from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from backend.schemas import UserCreate, UserLogin, UserOut
from backend.auth import hash_pw, verify_pw, create_token
from backend.database import SessionLocal
from backend.models import User

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db=Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar():
        raise HTTPException(400, "Email already registered")

    new_user = User(email=user.email, password=hash_pw(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post("/login")
async def login(data: UserLogin, db=Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar()

    if not user or not verify_pw(data.password, user.password):
        raise HTTPException(400, "Invalid credentials")

    token = create_token(user.id)
    return {"token": token, "user": UserOut.from_orm(user)}
