import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_session
from routers.users import router as users_router
from models import User
from auth import hash_password

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# DATABASE RESET ON STARTUP
# ------------------------------
@app.on_event("startup")
async def startup_event():
    reset = os.getenv("RESET_DB", "false").lower() == "true"

    if reset:
        print("🚨 RESET_DB ENABLED → Resetting database...")

        # Drop and recreate tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        print("✅ Tables recreated.")

        # Create default admin user
        async with AsyncSession(engine) as session:
            admin = User(
                email="admin@labelforce.com",
                hashed_password=hash_password("admin"),
                is_admin=True
            )
            session.add(admin)
            await session.commit()

        print("✅ Admin user created: admin@labelforce.com / admin")
        print("🚀 Database reset complete.")
    else:
        print("ℹ️ RESET_DB not enabled. Normal startup.")


# Routers
app.include_router(users_router, prefix="/auth")


@app.get("/")
async def root():
    return {"message": "Backend running"}
