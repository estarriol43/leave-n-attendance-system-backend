from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class LeaveType(Base):
    __tablename__ = 'leave_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    color_code = Column(String(7))

    leave_quotas = relationship('LeaveQuota', back_populates='leave_type')
    leave_requests = relationship('LeaveRequest', back_populates='leave_type')