import asyncio
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database import create_db_and_tables, get_session
from models import User
from auth import hash_password, get_current_user
from routers.users import router as users_router
from config import settings

app = FastAPI(title="LabelForce Backend")

app.include_router(users_router)

@app.on_event("startup")
async def on_startup():
    # create tables
    await create_db_and_tables()

    # auto-create admin user if missing
    async with (await get_session().__aenter__()) as session:  # use the generator's session
        q = select(User).where(User.email == "admin@labelforce.com")
        res = await session.exec(q)
        admin = res.first()
        if not admin:
            admin_user = User(
                email="admin@labelforce.com",
                hashed_password=hash_password("Admin1234!"),
                is_admin=True,
            )
            session.add(admin_user)
            await session.commit()

@app.get("/")
async def root():
    return {"status": "ok"}
