from sqlalchemy.orm import Session
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate

def create_attendance(db: Session, attendance: AttendanceCreate):
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance
