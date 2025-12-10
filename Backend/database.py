# Backend/database.py
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from config import settings

# Create engine (asyncpg)
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# Create session factory
AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# FIXED: This is now an async context manager, NOT a plain generator
@asynccontextmanager
async def get_session():
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
