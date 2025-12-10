# Backend/main.py
from fastapi import FastAPI
from routers.users import router as users_router
from database import create_db_and_tables
from config import settings
import asyncio

app = FastAPI(title="LabelForce Backend")

app.include_router(users_router)

@app.on_event("startup")
async def on_startup():
    # create tables (and optionally drop them if RESET_DB=True)
    await create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "LabelForce backend running"}
