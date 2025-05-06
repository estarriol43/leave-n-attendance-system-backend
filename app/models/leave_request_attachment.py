from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base

class LeaveRequestAttachment(Base):
    __tablename__ = 'leave_request_attachments'

    id = Column(Integer, primary_key=True)
    leave_request_id = Column(Integer, ForeignKey('leave_requests.id'), nullable=False)
    file_name = Column(String(255))
    file_type = Column(String(50))
    file_size = Column(Integer)
    uploaded_at = Column(DateTime, server_default=func.now())

    leave_request = relationship('LeaveRequest', back_populates='attachments')