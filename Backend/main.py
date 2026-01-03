from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
from models import Base

# Routers
from routers.users import router as users_router
from routers.datasets import router as datasets_router
from routers.data_items import router as data_items_router
from routers.labels import router as labels_router
from routers.annotations import router as annotations_router

# =====================================================
# App
# =====================================================

app = FastAPI(
    title="LabelForce API",
    description="AI Data Labeling Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# =====================================================
# CORS (Frontend access)
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://labelforce-frontend-5oaq.onrender.com",
        "http://localhost:5173",  # local Vite dev
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
# =====================================================

app.include_router(users_router, prefix="/auth", tags=["auth"])
app.include_router(datasets_router, prefix="/datasets", tags=["datasets"])
app.include_router(data_items_router, prefix="/data-items", tags=["data-items"])
app.include_router(labels_router, prefix="/labels", tags=["labels"])
app.include_router(annotations_router, prefix="/annotations", tags=["annotations"])

# =====================================================
# Health check
# =====================================================

@app.get("/", tags=["health"])
def home():
    return {"status": "ok", "message": "LabelForce backend running 🚀"}
