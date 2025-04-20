from pydantic import BaseModel
from datetime import date

class LeaveRequestCreate(BaseModel):
    user_id: int
    leave_type: str
    start_date: date
    end_date: date

class LeaveRequest(LeaveRequestCreate):
    id: int
    status: str

    class Config:
        orm_mode = True
