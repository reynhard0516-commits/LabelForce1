from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    display_name: Optional[str] = None
    password_hash: str = ""
    role: str = "worker"
    wallet_balance: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    title: str
    instructions: Optional[str] = None
    reward: float = 0.5
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskUnit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    payload: str
    status: str = "unassigned"
    assigned_to: Optional[int] = Field(default=None, foreign_key="user.id")
    submitted_result: Optional[str] = None
    ai_suggestion: Optional[str] = None
    reward: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Label(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_unit_id: int = Field(foreign_key="taskunit.id")
    label_type: str = "bbox"   # bbox, polygon, keypoints, classification
    data: str = ""  # JSON string with coords/class
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Versioning / snapshot table
class DatasetVersion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    tag: str
    metadata: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
