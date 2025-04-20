from sqlalchemy.orm import Session
from app.models.leave import LeaveRequest
from app.schemas.leave import LeaveRequestCreate

def create_leave_request(db: Session, leave_request: LeaveRequestCreate):
    db_leave_request = LeaveRequest(**leave_request.dict())
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request
