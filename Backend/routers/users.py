from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from database import get_db
from models.user import User
from auth import verify_password, get_password_hash, create_access_token

router = APIRouter()

@router.post("/register")
async def register(data: dict, db=Depends(get_db)):
    user = User(
        email=data["email"],
        password=get_password_hash(data["password"])
    )
    db.add(user)
    await db.commit()
    return {"message": "User created"}

@router.post("/login")
async def login(data: dict, db=Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data["email"]))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data["password"], user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token}
