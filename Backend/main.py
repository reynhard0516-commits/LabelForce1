from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from Backend.routers.users import router as users_router
from Backend.database import init_db
from Backend.config import RESET_DB

app = FastAPI(title="LabelForce Backend")

origins = ["*"]  # You can restrict later

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)

@app.on_event("startup")
async def startup_event():
    await init_db(drop_first=RESET_DB)
