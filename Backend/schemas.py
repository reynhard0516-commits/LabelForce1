from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    is_admin: bool

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str]


class TaskCreate(BaseModel):
    project_id: int
    file_path: str
