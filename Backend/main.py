from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

# Routers
from routers.users import router as users_router
from routers.datasets import router as datasets_router
from routers.data_items import router as data_items_router
from routers.labels import router as labels_router
from routers.annotations import router as annotations_router
from routers.export import router as export_router  # ✅ ADD THIS
from routers.ai import router as ai_router

app.include_router(ai_router)
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
# Startup: create tables
# =====================================================

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# =====================================================
# Routers
# =====================================================

app.include_router(users_router, prefix="/auth", tags=["auth"])
app.include_router(datasets_router, tags=["datasets"])
app.include_router(data_items_router, tags=["items"])
app.include_router(labels_router, tags=["labels"])
app.include_router(annotations_router, tags=["annotations"])
app.include_router(export_router, tags=["export"])  # ✅ EXPORT ENABLED

# =====================================================
# Health check
# =====================================================

@app.get("/")
def health():
    return {"status": "LabelForce backend running 🚀"}
