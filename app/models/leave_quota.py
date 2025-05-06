from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class LeaveQuota(Base):
    __tablename__ = 'leave_quotas'
    __table_args__ = (
        UniqueConstraint('user_id', 'leave_type_id', 'year', name='uq_user_leave_year'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    leave_type_id = Column(Integer, ForeignKey('leave_types.id'), nullable=False)
    year = Column(Integer, nullable=False)
    quota = Column(Integer, nullable=False)

    user = relationship('User', back_populates='leave_quotas')
    leave_type = relationship('LeaveType', back_populates='leave_quotas')