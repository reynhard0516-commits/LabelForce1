from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from config import settings
from database import create_db_and_tables, get_session, AsyncSessionLocal
from models import User
from auth import hash_password, verify_password, create_access_token
from schemas import UserCreate, Token

app = FastAPI(title="LabelForce Backend")


@app.on_event("startup")
async def on_startup():
    # create tables
    await create_db_and_tables()

    # AUTO-CREATE ADMIN IF MISSING
    async with AsyncSessionLocal() as session:
        query = select(User).where(User.email == "admin@labelforce.com")
        result = await session.exec(query)
        admin = result.first()
        if not admin:
            admin = User(
                email="admin@labelforce.com",
                hashed_password=hash_password("Password123"),  # temp admin password (change)
                is_admin=True,
            )
            session.add(admin)
            await session.commit()


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    # check exists
    exists = await session.exec(select(User).where(User.email == payload.email))
    if exists.first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"message": "user registered", "id": user.id}


@app.post("/login", response_model=Token)
async def login(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    res = await session.exec(select(User).where(User.email == payload.email))
    user = res.first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=user.email)
    return {"access_token": token, "token_type": "bearer"}
