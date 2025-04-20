from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    leave_type = Column(String)  # 'annual', 'sick', 'personal', etc.
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String)  # 'pending', 'approved', 'rejected'
