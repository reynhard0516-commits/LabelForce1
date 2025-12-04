
from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True)
    sku = Column(String)
    user_id = Column(Integer)
    result = Column(String)
    timestamp = Column(DateTime, server_default=func.now())
