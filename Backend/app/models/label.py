
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True)
    sku = Column(String, unique=True)
    product_name = Column(String)
    enabled = Column(Boolean, default=True)
    group_name = Column(String, nullable=True)
