from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

from routers.users import router as users_router
from routers.datasets import router as datasets_router
from routers.data_items import router as data_items_router

app = FastAPI(title="LabelForce API")

# =====================================================
# CORS
# =====================================================

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

# =====================================================
# Startup: create DB tables
# =====================================================

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# =====================================================
# Routers
# IMPORTANT: do NOT add prefixes here
# =====================================================

app.include_router(users_router)      # /auth/...
app.include_router(datasets_router)   # /datasets/...
app.include_router(data_items_router) # /items/...

# =====================================================
# Health check
# =====================================================

@app.get("/")
def health():
    return {"status": "LabelForce backend running 🚀"}
