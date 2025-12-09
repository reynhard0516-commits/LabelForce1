from sqlmodel import SQLModel, create_engine, Session
from config import DATABASE_URL

# Sync engine (Render works well with this)
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
