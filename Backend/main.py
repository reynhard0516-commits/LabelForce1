from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import create_db_and_tables, get_session
from models import User
from sqlmodel import select
import uvicorn

app = FastAPI()

# ---------------------------
# CORS (allow all for testing)
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Run DB table creation on startup
# ---------------------------
@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
    print("Database tables created")


# ---------------------------
# Example route: get all users
# ---------------------------
@app.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User))
    return result.all()


# ---------------------------
# Example route: create a test user
# ---------------------------
@app.post("/users")
async def create_user(email: str, password: str, session: AsyncSession = Depends(get_session)):
    # Check if user exists
    result = await session.exec(select(User).where(User.email == email))
    existing = result.first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=email,
        hashed_password=password,   # ⚠️  You must hash passwords in real apps
        is_admin=False
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


# ---------------------------
# Root route
# ---------------------------
@app.get("/")
async def root():
    return {"message": "LabelForce Backend Running!"}


# ---------------------------
# Render runs uvicorn automatically,
# but this allows local testing
# ---------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
