from fastapi import FastAPI
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import create_db_and_tables, AsyncSessionLocal   # matches your database.py
from models import User
from auth import hash_password  # you already imported this in previous screenshots
from routers.users import router as users_router  # matches your repo import shown earlier

app = FastAPI(title="LabelForce Backend")

# include your users router (assumes routers/users.py exists and exports `router`)
app.include_router(users_router)


@app.on_event("startup")
async def on_startup():
    """
    Create database tables and ensure an admin user exists.
    This will only create the admin if it is not already present (Option A).
    """
    # create tables (uses your create_db_and_tables function)
    await create_db_and_tables()

    # ensure admin user exists (only create if not present)
    admin_email = "admin@labelforce.com"
    admin_password = "admin"  # change this after first deploy in Render env or via UI

    async with AsyncSessionLocal() as session:  # create a session for checking/creating admin
        # look up existing admin by email
        query = select(User).where(User.email == admin_email)
        result = await session.exec(query)
        admin = result.first()

        if admin is None:
            # create admin user (only if not found)
            new_admin = User(
                email=admin_email,
                hashed_password=hash_password(admin_password),
                is_admin=True,
            )
            session.add(new_admin)
            await session.commit()
            app.logger = getattr(app, "logger", None)
            print(f"[startup] Created admin user: {admin_email}")
        else:
            print(f"[startup] Admin user already exists: {admin_email}")


@app.get("/")
async def root():
    return {"status": "ok"}
