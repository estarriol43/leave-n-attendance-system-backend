import enum
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, Enum, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class LeaveStatus(enum.Enum):
    pending = 'Pending'
    approved = 'Approved'
    rejected = 'Rejected'

class LeaveRequest(Base):
    __tablename__ = 'leave_requests'

    id = Column(Integer, primary_key=True)
    request_id = Column(String(50), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    leave_type_id = Column(Integer, ForeignKey('leave_types.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_half_day = Column(Boolean, default=False)
    end_half_day = Column(Boolean, default=False)
    days_count = Column(Integer) # 這裡可以是小數
    reason = Column(Text)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.pending)
    proxy_user_id = Column(Integer, ForeignKey('users.id'))
    approver_id = Column(Integer, ForeignKey('users.id'))
    approved_at = Column(DateTime)
    rejection_reason = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # relationships
    user = relationship("User", back_populates="leave_requests", foreign_keys=[user_id])
    approver = relationship("User", back_populates="leave_requests_as_approver", foreign_keys=[approver_id])
    leave_type = relationship('LeaveType', back_populates='leave_requests')
    proxy_user = relationship('User', foreign_keys=[proxy_user_id])
    attachments = relationship('LeaveRequestAttachment', back_populates='leave_request')