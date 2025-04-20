# app/routes/attendance.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.crud.attendance import create_attendance
from app.schemas.attendance import AttendanceCreate

router = APIRouter()

@router.post("/check-in")
def check_in(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    return create_attendance(db=db, attendance=attendance)
