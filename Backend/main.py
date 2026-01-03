from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

from routers import users, datasets, data_items, labels, annotations

app = FastAPI(title="LabelForce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router, prefix="/auth")
app.include_router(datasets.router, prefix="/datasets")
app.include_router(data_items.router, prefix="/data-items")
app.include_router(labels.router, prefix="/labels")
app.include_router(annotations.router, prefix="/annotations")

@app.get("/")
def health():
    return {"status": "ok"}
