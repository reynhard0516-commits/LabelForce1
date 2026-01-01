from fastapi import FastAPI
from database import engine
from models import Base

# Routers
from routers.users import router as users_router
from routers.datasets import router as datasets_router
from routers.data_items import router as data_items_router
from routers.labels import router as labels_router
from routers.annotations import router as annotations_router

app = FastAPI(
    title="LabelForce API",
    description="AI Data Labeling Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# =====================================================
# Startup: create tables
# =====================================================

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# =====================================================
# Routers
# =====================================================

app.include_router(users_router)
app.include_router(datasets_router)
app.include_router(data_items_router)
app.include_router(labels_router)
app.include_router(annotations_router)

# =====================================================
# Health check
# =====================================================

@app.get("/")
def home():
    return {"message": "LabelForce backend running 🚀"}
