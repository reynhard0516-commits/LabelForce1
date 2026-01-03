from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class DataItem(Base):
    __tablename__ = "data_items"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    content = Column(String, nullable=False)
