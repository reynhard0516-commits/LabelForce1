from fastapi import FastAPI
from database import engine
from models import Base
from routers.users import router as users_router
from auth import router as auth_router   # ✅ ADD THIS

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users_router)
app.include_router(auth_router)          # ✅ ADD THIS

@app.get("/")
def home():
    return {"message": "Backend running"}
