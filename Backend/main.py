from fastapi import FastAPI
from database import engine
from models import Base
from routers.users import router as users_router
from routers.datasets import router as datasets_router

app = FastAPI(
    title="LabelForce API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users_router)
app.include_router(datasets_router)

@app.get("/")
def home():
    return {"message": "Backend running"}
