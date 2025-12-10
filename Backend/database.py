# Backend/database.py
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
import asyncio

# Make sure DATABASE_URL uses async driver: postgresql+asyncpg://...
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def create_db_and_tables():
    # Use run_sync to run metadata operations in sync context
    async with engine.begin() as conn:
        if settings.RESET_DB:
            # Danger: drops all tables — use only when you want a clean DB
            await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
