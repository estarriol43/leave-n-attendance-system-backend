from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    employee_id: Optional[str] = None


class LeaveTypeBase(BaseModel):
    id: int
    name: str


class AttachmentBase(BaseModel):
    id: int
    file_name: str
    file_type: str
    file_size: int
    uploaded_at: datetime


class LeaveRequestDetail(BaseModel):
    id: int
    request_id: str
    user: UserBase
    leave_type: LeaveTypeBase
    start_date: date
    end_date: date
    days_count: int
    reason: str
    status: str
    proxy_person: Optional[UserBase] = None
    approver: Optional[UserBase] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    attachments: List[AttachmentBase] = []

