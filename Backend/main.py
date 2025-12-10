from fastapi import FastAPI
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import create_db_and_tables, get_session, AsyncSessionLocal
from models import User
from auth import hash_password
from routers.users import router as users_router

app = FastAPI(title="LabelForce Backend")
app.include_router(users_router)

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

    async with AsyncSessionLocal() as session:
        from sqlmodel import select

        query = select(User).where(User.email == "admin@labelforce.com")
        result = await session.exec(query)
        admin = result.first()

        if not admin:
            admin = User(
                email="admin@labelforce.com",
                hashed_password=hash_password("Admin123!"),  # short password
                is_admin=True
            )
            session.add(admin)
            await session.commit()

@app.get("/")
async def root():
    return {"status": "ok"}
