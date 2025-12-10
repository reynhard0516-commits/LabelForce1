from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import create_db_and_tables, get_session
from models import User
from sqlmodel import select
import uvicorn

app = FastAPI()

# ---------------------------
# CORS (allow all for testing)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Run DB table creation on startup
# ---------------------------
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    print("Database tables created")


# ---------------------------
# Example route: get all users
# ---------------------------
@app.get("/users")
async def get_users(session: AsyncSession =
