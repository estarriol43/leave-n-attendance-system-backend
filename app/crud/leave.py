from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from datetime import datetime
from ..models.leave_request import LeaveRequest
from ..models.user import User
from ..models.leave_type import LeaveType
from ..models.leave_quota import LeaveQuota 
from ..schemas.leave import LeaveRequestDetail, LeaveRequestCreate, LeaveRequestOut
from uuid import uuid4

def generate_request_id():
    id = str(uuid4().hex[:16].upper())
    return id

def create_leave_request(db: Session, user_id: int, data: LeaveRequestCreate):
    # 計算請假天數（整天制）
    days_requested = (data.end_date - data.start_date).days + 1
    current_year = datetime.now().year

    # get leave_type
    leave_type = db.query(LeaveType).filter(LeaveType.id == data.leave_type_id).first()
    if not leave_type: 
        raise ValueError("Invalid leave_type_id")

    # check proxy
    proxy_user = db.query(User).filter(User.id == data.proxy_user_id).first()
    if not proxy_user:
        raise ValueError("Invalid leave_type_id or proxy_user_id")

    # check quota per year
    quota = db.query(LeaveQuota).filter_by(
        user_id=user_id,
        leave_type_id=data.leave_type_id,
        year=current_year
    ).first()
    if not quota:
        raise ValueError("No leave quota found for this leave type")
    
    # calculate remaining quota
    approved_requests = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.user_id == user_id,
            LeaveRequest.leave_type_id == data.leave_type_id,
            func.extract('year', LeaveRequest.start_date) == current_year,
            LeaveRequest.status == 'approved'
        )
        .all()
    )

    used_days = sum([r.days_count for r in approved_requests])
    remaining_days = quota.quota - used_days
    if remaining_days < days_requested:
        raise ValueError(f"Not enough leave balance. Remaining: {remaining_days}, Requested: {days_requested}")

    new_request = LeaveRequest(
        request_id = generate_request_id(),
        user_id = user_id,
        leave_type_id = data.leave_type_id,
        start_date = data.start_date,
        end_date = data.end_date,
        days_count = days_requested,
        reason = data.reason,
        proxy_user_id = data.proxy_user_id,
        status="pending",
        created_at=datetime.utcnow()
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    db.refresh(leave_type)
    db.refresh(proxy_user)
    return LeaveRequestOut(
        id = new_request.id,
        request_id = new_request.request_id,
        leave_type = leave_type,
        start_date = new_request.start_date,
        end_date = new_request.end_date,
        days_count = new_request.days_count,
        reason = new_request.reason,
        status = new_request.status,
        proxy_person = proxy_user,
        created_at = new_request.created_at
    )

def get_leave_request_by_id(db: Session, leave_request_id: int) -> LeaveRequestDetail:
    leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == leave_request_id).first()
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    
    return leave_request
