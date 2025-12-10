from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from Backend.routers import users as users_router
from Backend.database import init_db

app = FastAPI(title="LabelForce Backend")

origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router.router)

@app.on_event("startup")
async def startup_event():
    reset = os.getenv("RESET_DB", "false").lower() in ("1", "true", "yes")
    await init_db(drop_first=reset)
