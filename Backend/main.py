from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Backend.database import engine, Base
from Backend.routers.users import router as users_router
from Backend.routers.datasets import router as datasets_router

app = FastAPI(
    title="LabelForce API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://labelforce-frontend-5oaq.onrender.com",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(users_router)
app.include_router(datasets_router)


@app.get("/")
def home():
    return {"message": "LabelForce backend running 🚀"}
