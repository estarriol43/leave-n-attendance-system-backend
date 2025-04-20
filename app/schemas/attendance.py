from pydantic import BaseModel
from datetime import datetime

class AttendanceCreate(BaseModel):
    user_id: int
    date: datetime
    status: str

class Attendance(AttendanceCreate):
    id: int

    class Config:
        orm_mode = True
