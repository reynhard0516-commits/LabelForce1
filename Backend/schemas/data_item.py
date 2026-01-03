from pydantic import BaseModel

class DataItemCreate(BaseModel):
    content: str

class DataItemOut(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True
