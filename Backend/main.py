from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select

from database import create_db_and_tables, get_session
from models import User
from auth import hash_password, verify_password, create_access_token

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

    # AUTO-CREATE ADMIN IF IT DOESN'T EXIST
    with get_session() as session:
        admin = session.exec(
            select(User).where(User.email == "admin@labelforce.com")
        ).first()

        if not admin:
            admin = User(
                email="admin@labelforce.com",
                hashed_password=hash_password("Admin1234!"),
                is_admin=True
            )
            session.add(admin)
            session.commit()

@app.post("/register")
def register(email: str, password: str, session=Depends(get_session)):
    exists = session.exec(select(User).where(User.email == email)).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=email,
        hashed_password=hash_password(password),
        is_admin=False
    )
    session.add(user)
    session.commit()

    return {"message": "Registered successfully"}
