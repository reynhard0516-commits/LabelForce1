from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pydantic import BaseModel
from typing import Optional, List
import os, uuid, shutil

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./labelforce.db")
SECRET_KEY = os.getenv("LF_SECRET", "change_me_secret")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MIN = int(os.getenv("ACCESS_EXPIRE_MIN", "1440"))

engine = create_engine(DATABASE_URL, echo=False)

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="LabelForce Backend (FastAPI)")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    display_name: Optional[str] = None
    password_hash: str = ""
    role: str = "worker"
    wallet_balance: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskUnit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    payload: str
    status: str = "unassigned"
    assigned_to: Optional[int] = None
    submitted_result: Optional[str] = None
    ai_suggestion: Optional[str] = None
    reward: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Schemas
class UserCreate(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SubmitPayload(BaseModel):
    result: dict

# DB setup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Auth helpers
def get_password_hash(pw: str):
    return pwd.hash(pw)

def verify_password(plain, hashed):
    return pwd.verify(plain, hashed)

def create_access_token(data: dict, expires_minutes: int = ACCESS_EXPIRE_MIN):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    creds_exc = HTTPException(status_code=401, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise creds_exc
    except JWTError:
        raise creds_exc
    with Session(engine) as session:
        user = session.get(User, int(sub))
        if not user:
            raise creds_exc
        return user

# Auth endpoints
@app.post("/auth/register", response_model=Token)
def register(u: UserCreate):
    with Session(engine) as session:
        exists = session.exec(select(User).where(User.email == u.email)).first()
        if exists:
            raise HTTPException(status_code=400, detail="Email exists")
        user = User(email=u.email, display_name=u.display_name or u.email.split("@")[0], password_hash=get_password_hash(u.password))
        session.add(user); session.commit(); session.refresh(user)
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}

@app.post("/auth/login", response_model=Token)
def login(u: UserCreate):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == u.email)).first()
        if not user or not verify_password(u.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Bad credentials")
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}

# Task endpoints
@app.post("/tasks/upload")
def upload_tasks(file: UploadFile = File(...), reward: float = 0.5, current_user: User = Depends(get_current_user)):
    content = file.file.read().decode("utf-8").strip().splitlines()
    with Session(engine) as session:
        created = 0
        for line in content:
            tu = TaskUnit(payload=line.strip(), reward=reward)
            session.add(tu); created += 1
        session.commit()
    return {"ok": True, "created": created}

@app.get("/tasks/available", response_model=List[TaskUnit])
def available(limit: int = 10, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        items = session.exec(select(TaskUnit).where(TaskUnit.status == "unassigned").limit(limit)).all()
        return items

@app.post("/tasks/{unit_id}/claim")
def claim(unit_id: int, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        unit = session.get(TaskUnit, unit_id)
        if not unit or unit.status != "unassigned":
            raise HTTPException(status_code=404, detail="Not available")
        unit.status = "assigned"; unit.assigned_to = current_user.id
        session.add(unit); session.commit(); session.refresh(unit)
        return {"ok": True, "unit_id": unit.id}

@app.post("/tasks/{unit_id}/submit")
def submit(unit_id: int, payload: SubmitPayload, current_user: User = Depends(get_current_user)):
    with Session(engine) as session:
        unit = session.get(TaskUnit, unit_id)
        if not unit or unit.assigned_to != current_user.id:
            raise HTTPException(status_code=403, detail="Not assigned to you")
        unit.submitted_result = str(payload.result)
        unit.status = "submitted"
        session.add(unit)
        user = session.get(User, current_user.id)
        user.wallet_balance += unit.reward
        session.add(user)
        session.commit()
        return {"ok": True}

# AI prelabel placeholder
@app.post("/ai/prelabel")
def prelabel(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    tmp = f"/tmp/{uuid.uuid4().hex}_{file.filename}"
    with open(tmp, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # placeholder result
    res = {"boxes": [{"label": "demo", "confidence": 0.87, "bbox": [50,50,200,150]}]}
    try:
        os.remove(tmp)
    except:
        pass
    return {"prelabel": res}

@app.get("/users/me")
def whoami(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "wallet": current_user.wallet_balance}
