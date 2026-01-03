from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from database import get_db
from models.dataset import Dataset
from models.user import User
from auth import decode_token

router = APIRouter()

@router.get("")
async def list_datasets(token=Depends(decode_token), db=Depends(get_db)):
    email = token["sub"]
    user = (await db.execute(select(User).where(User.email == email))).scalar_one()
    return (await db.execute(select(Dataset).where(Dataset.owner_id == user.id))).scalars().all()
