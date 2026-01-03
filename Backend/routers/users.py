from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(data: AuthRequest):
    return {"access_token": "1", "token_type": "bearer"}


@router.post("/register")
async def register(data: AuthRequest):
    return {"message": "User registered"}


@router.get("/me")
async def me():
    return {"id": 1, "email": "test@example.com"}
