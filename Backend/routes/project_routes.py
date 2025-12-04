from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from backend.database import SessionLocal
from backend.models import Project
from backend.schemas import ProjectCreate

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/")
async def create_project(data: ProjectCreate, db=Depends(get_db)):
    new_proj = Project(name=data.name, description=data.description)
    db.add(new_proj)
    await db.commit()
    await db.refresh(new_proj)
    return new_proj

@router.get("/")
async def get_projects(db=Depends(get_db)):
    result = await db.execute(select(Project))
    return result.scalars().all()
