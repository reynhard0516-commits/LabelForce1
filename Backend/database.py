import os
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from Backend.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session

async def init_db(drop_first=False):
    from Backend import models

    async with engine.begin() as conn:
        if drop_first:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
