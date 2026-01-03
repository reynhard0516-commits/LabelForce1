from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class DataItem(Base):
    __tablename__ = "data_items"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    type = Column(String, default="text")
    content = Column(String)
