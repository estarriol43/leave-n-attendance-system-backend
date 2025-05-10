from pydantic import BaseModel, ConfigDict
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
    # attachments: List[AttachmentBase] = []

class LeaveRequestCreate(BaseModel):
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str
    proxy_user_id: int


class LeaveTypeBasic(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProxyUserOut(BaseModel):
    id: int
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class LeaveRequestOut(BaseModel):
    id: int
    request_id: str
    leave_type: LeaveTypeBasic
    start_date: date
    end_date: date
    days_count: float
    reason: str
    status: str
    proxy_person: ProxyUserOut
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LeaveRequestListItem(BaseModel):
    id: int
    request_id: str
    leave_type: LeaveTypeBasic
    start_date: date
    end_date: date
    days_count: float
    reason: str
    status: str
    proxy_person: ProxyUserOut 
    approver: Optional[ProxyUserOut] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    rejection_reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PaginationMeta(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int


class LeaveRequestListResponse(BaseModel):
    leave_requests: List[LeaveRequestListItem]
    pagination: PaginationMeta


class LeaveRequestTeamItem(LeaveRequestListItem):
    user: ProxyUserOut 

class LeaveRequestTeamListResponse(BaseModel):
    leave_requests: List[LeaveRequestTeamItem]
    pagination: PaginationMeta

class LeaveRequestApprovalResponse(BaseModel):
    id: int
    request_id: str
    status: str
    approver: ProxyUserOut
    approved_at: datetime

    model_config = ConfigDict(from_attributes=True)