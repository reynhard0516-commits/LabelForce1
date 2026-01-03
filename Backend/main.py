from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

# =====================================================
# ROUTERS
# =====================================================

from routers.users import router as users_router
from routers.datasets import router as datasets_router
from routers.data_items import router as data_items_router
from routers.labels import router as labels_router
from routers.annotations import router as annotations_router
from routers.export import router as export_router
from routers.ai import router as ai_router

# =====================================================
# APP
# =====================================================

app = FastAPI(
    title="LabelForce API",
    description="AI Data Labeling Platform Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# =====================================================
# CORS (FRONTEND ACCESS)
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
# STARTUP — CREATE TABLES
# =====================================================

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# =====================================================
# ROUTE REGISTRATION
# =====================================================

app.include_router(users_router, prefix="/auth", tags=["auth"])
app.include_router(datasets_router, prefix="/datasets", tags=["datasets"])
app.include_router(data_items_router, prefix="/items", tags=["items"])
app.include_router(labels_router, prefix="/labels", tags=["labels"])
app.include_router(annotations_router, prefix="/annotations", tags=["annotations"])
app.include_router(export_router, prefix="/export", tags=["export"])
app.include_router(ai_router, prefix="/ai", tags=["ai"])

# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/")
def health():
    return {
        "status": "LabelForce backend running 🚀",
        "docs": "/docs",
    }
