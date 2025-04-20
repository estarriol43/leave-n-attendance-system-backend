# app/routes/leave.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.leave import create_leave_request
from app.schemas.leave import LeaveRequestCreate

router = APIRouter()

@router.post("/request")
def request_leave(leave_request: LeaveRequestCreate, db: Session = Depends(get_db)):
    return create_leave_request(db=db, leave_request=leave_request)
