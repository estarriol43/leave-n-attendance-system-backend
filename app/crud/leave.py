from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from ..models.leave_request import LeaveRequest
from ..models.user import User
from ..schemas.leave import LeaveRequestDetail


def get_leave_request_by_id(db: Session, leave_request_id: int) -> LeaveRequestDetail:
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    return leave_request
