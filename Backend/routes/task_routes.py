from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from backend.database import SessionLocal
from backend.models import Task
from backend.schemas import TaskCreate

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/")
async def create_task(data: TaskCreate, db=Depends(get_db)):
    task = Task(project_id=data.project_id, file_path=data.file_path)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

@router.get("/{project_id}")
async def get_tasks(project_id: int, db=Depends(get_db)):
    result = await db.execute(select(Task).where(Task.project_id == project_id))
    return result.scalars().all()
