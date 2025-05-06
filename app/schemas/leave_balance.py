from pydantic import BaseModel
from typing import List
from datetime import date


class LeaveRequestSummary(BaseModel):
    id: int
    request_id: str
    start_date: date
    end_date: date
    days_count: float
    status: str

    class Config:
        orm_mode = True


class LeaveTypeInfo(BaseModel):
    id: int
    name: str
    color_code: str

    class Config:
        orm_mode = True


class LeaveBalanceItem(BaseModel):
    leave_type: LeaveTypeInfo
    quota: int
    used_days: float
    remaining_days: float
    leave_requests: List[LeaveRequestSummary]

    class Config:
        orm_mode = True


class LeaveBalanceResponse(BaseModel):
    year: int
    balances: List[LeaveBalanceItem]
