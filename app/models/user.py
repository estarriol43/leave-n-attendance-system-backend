from sqlalchemy import String, Boolean, Date, Integer, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from typing import Optional
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_manager: Mapped[bool] = mapped_column(Boolean, server_default="False", nullable=False)
    annual_leave_quota: Mapped[int] = mapped_column(Integer, server_default="7", nullable=False)
    sick_leave_quota: Mapped[int] = mapped_column(Integer, server_default="30", nullable=False)
    personal_leave_quota: Mapped[int] = mapped_column(Integer, server_default="14", nullable=False)
    public_holiday_quota: Mapped[int] = mapped_column(Integer, server_default="5", nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    department: Mapped["Department"] = relationship("Department", back_populates="users")
    leave_requests: Mapped[list["LeaveRequest"]] = relationship("LeaveRequest", back_populates="user", foreign_keys="LeaveRequest.user_id")
    proxy_requests: Mapped[list["LeaveRequest"]] = relationship("LeaveRequest", back_populates="proxy_user", foreign_keys="LeaveRequest.proxy_user_id")
    approvals: Mapped[list["LeaveRequest"]] = relationship("LeaveRequest", back_populates="approver", foreign_keys="LeaveRequest.approver_id")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="user")
    audit_logs: Mapped[list["AuditLog"]] = relationship("AuditLog", back_populates="user")
    
    manager_relations: Mapped[list["Manager"]] = relationship("Manager", back_populates="user", foreign_keys=["Manager.user_id"])
    subordinate_relations: Mapped[list["Manager"]] = relationship("Manager", back_populates="manager", foreign_keys=["Manager.manager_id"])
