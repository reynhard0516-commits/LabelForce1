# Backend/database.py
import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

DATABASE_URL = os.getenv("DATABASE_URL")  # must be set in Render env
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

# If using Postgres with asyncpg, use: postgresql+asyncpg://user:pass@host/db
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False, future=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def init_db(drop_first: bool = False) -> None:
    """
    Initialize DB tables. If drop_first True, drop all tables then create.
    """
    async with engine.begin() as conn:
        if drop_first:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
