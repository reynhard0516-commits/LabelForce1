# Backend/main.py
from fastapi import FastAPI
from routers.users import router as users_router
from database import create_db_and_tables, get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import asyncio

from auth import hash_password
from models import User
from config import settings

app = FastAPI(title="LabelForce Backend")

app.include_router(users_router)


@app.on_event("startup")
async def on_startup():
    # create DB tables
    await create_db_and_tables()

    # create admin user if not exists
    async with get_session() as session:  # returns an async context manager (AsyncSession)
        q = select(User).where(User.email == "admin@labelforce.com")
        result = await session.exec(q)
        admin = result.first()
        if not admin:
            admin_user = User(
                email="admin@labelforce.com",
                hashed_password=hash_password("Admin123!"),  # change if you want
                is_admin=True
            )
            session.add(admin_user)
            await session.commit()
