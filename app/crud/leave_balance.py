from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from ..models import leave_requests, leave_types, users
from ..schemas.leave_balance import LeaveBalanceResponse, LeaveBalanceItem, LeaveTypeInfo, LeaveRequestSummary


def get_leave_balances(db: Session, user_id: int) -> LeaveBalanceResponse:
    user = db.query(users).filter(users.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    # 取得所有假別類型
    leave_type_list = db.query(leave_types).all()

    balances = []

    for lt in leave_type_list:
        # 查詢該假別的請假紀錄
        requests = db.query(leave_requests).filter(
            leave_requests.user_id == user_id,
            leave_requests.leave_type_id == lt.id,
            func.extract('year', leave_requests.start_date) == datetime.now().year,
            leave_requests.status == 'Approved'
        ).all()

        used_days = sum([r.days_count for r in requests])
        
        # 根據使用者欄位取得對應假別的配額
        if lt.name == "Annual Leave":
            quota = user.annual_leave_quota
        elif lt.name == "Sick Leave":
            quota = user.sick_leave_quota
        elif lt.name == "Personal Leave":
            quota = user.personal_leave_quota
        elif lt.name == "Public Holiday":
            quota = user.public_holiday_quota
        else:
            quota = 0

        remaining = quota - used_days

        balances.append(LeaveBalanceItem(
            leave_type=LeaveTypeInfo.from_orm(lt),
            quota=quota,
            used_days=used_days,
            remaining_days=remaining,
            leave_requests=[LeaveRequestSummary.from_orm(r) for r in requests]
        ))

    return LeaveBalanceResponse(year=datetime.now().year, balances=balances)
