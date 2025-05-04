from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    employee_id = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    position = Column(String(100))
    hire_date = Column(Date)
    is_manager = Column(Boolean, default=False)

    # relationships
    department = relationship('Department', back_populates='users')
    subordinate_relations = relationship('Manager', foreign_keys='Manager.user_id', back_populates='user')
    manager_relations = relationship('Manager', foreign_keys='Manager.manager_id', back_populates='manager')
    # 1對多關聯：一個User可以有多個LeaveQuota
    leave_quotas = relationship('LeaveQuota', back_populates='user')
    # 1對多關聯：一個User可以有多個LeaveRequest
    leave_requests = relationship(
        "LeaveRequest",
        back_populates="user",  # 反向關聯
        foreign_keys="[LeaveRequest.user_id]",  # 指定應該使用哪個外鍵
        cascade="all, delete-orphan",
    )

    # 1對多關聯：一個User可以有多個LeaveRequest作為審核者
    leave_requests_as_approver = relationship(
        "LeaveRequest",
        back_populates="approver",  # 反向關聯
        foreign_keys="[LeaveRequest.approver_id]",  # 指定應該使用哪個外鍵
        cascade="all, delete-orphan",
    )
    notifications = relationship('Notification', back_populates='user')