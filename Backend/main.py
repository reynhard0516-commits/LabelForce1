from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.users import router as users_router
from .database import init_db

app = FastAPI(title="LabelForce API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

# Register routes
app.include_router(users_router)

@app.get("/")
def root():
    return {"status": "Backend running"}
