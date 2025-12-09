from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select

from database import create_db_and_tables, get_session
from models import User
from config import settings
from auth import hash_password, verify_password, create_access_token

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

    # AUTO-CREATE ADMIN IF IT DOESN'T EXIST
    from sqlmodel import select
    from auth import hash_password
from models import User
from database import get_session

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

    user = User(email=email, hashed_password=hash_password(password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User registered"}

@app.post("/login")
def login(email: str, password: str, session=Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid login")

    token = create_access_token({"sub": email})
    return {"access_token": token, "token_type": "bearer"}
