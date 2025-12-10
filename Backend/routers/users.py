from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from database import get_session
from models import User
from schemas import UserCreate, Token
from auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter
