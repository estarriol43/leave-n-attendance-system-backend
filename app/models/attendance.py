from sqlalchemy import Column, Integer, DateTime, String
from app.database import Base

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    date = Column(DateTime)
    status = Column(String)  # 'present', 'absent', etc.