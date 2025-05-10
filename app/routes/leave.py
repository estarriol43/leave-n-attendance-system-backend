from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from ..crud import user as user_crud
from ..crud import leave as leave_crud
from ..schemas.user import UserOut, TeamListResponse
from ..schemas.leave import LeaveRequestDetail, LeaveRequestOut, LeaveRequestCreate, LeaveRequestListResponse, LeaveRequestTeamListResponse
from ..utils.dependencies import get_current_user
from ..models.user import User
from ..database import get_db

router = APIRouter(
    prefix="/api/leave-requests",
    tags=["leave-requests"]
)

@router.post("", response_model=LeaveRequestOut, status_code=status.HTTP_201_CREATED)
def request_leave(
    payload: LeaveRequestCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Create a new leave request for current user
    """
    try: 
        return leave_crud.create_leave_request(db, current_user.id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=LeaveRequestListResponse)
def list_my_leave_requests(
    status: Optional[str] = Query(None, description="Filter"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge = 1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user:  User = Depends(get_current_user)
):
    """
    Get list of leave requests for the current user.
    """
    try:
        result = leave_crud.get_leave_requests_for_user(
            db=db,
            user_id=current_user.id,
            status=status,
            start_date=start_date,
            end_date=end_date,
            page=page,
            per_page=per_page,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "leave_requests": result["items"],
        "pagination": {
            "total": result["total"],
            "page": result["page"],
            "per_page": result["per_page"],
            "total_pages": result["total_pages"]
        }
    }

@router.get("/team", response_model=LeaveRequestTeamListResponse)
def list_team_leave_requests(
    user_id: Optional[int] = Query(None, description="target user_id"),
    status: Optional[str] = Query(None, description="Filter"),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    page: int = Query(1, ge = 1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user:  User = Depends(get_current_user)    
): 
    """
    Get list of leave requests of team members.
    """
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Access restricted to managers.")
    
    try:
        result = leave_crud.get_team_leave_requests(
            db=db,
            manager_id=current_user.id,
            user_id=user_id,
            status=status,
            start_date=start_date,
            end_date=end_date,
            page=page,
            per_page=per_page
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    return {
        "leave_requests": result["items"],
        "pagination": {
            "total": result["total"],
            "page": result["page"],
            "per_page": result["per_page"],
            "total_pages": result["total_pages"]
        }
    }


@router.get("/pending", response_model=LeaveRequestTeamListResponse)
def list_pending_leave_requests(
    user_id: Optional[int] = Query(None, description="target user_id"),
    page: int = Query(1, ge = 1),
    per_page: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user:  User = Depends(get_current_user)    
): 
    """
    Get list of pending leave requests of team members.
    """
    if not current_user.is_manager:
        raise HTTPException(status_code=403, detail="Access restricted to managers.")
    
    try:
        result = leave_crud.get_team_leave_requests(
            db=db,
            manager_id=current_user.id,
            user_id=user_id,
            status="pending",
            page=page,
            per_page=per_page
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    return {
        "leave_requests": result["items"],
        "pagination": {
            "total": result["total"],
            "page": result["page"],
            "per_page": result["per_page"],
            "total_pages": result["total_pages"]
        }
    }

@router.get("/{leave_request_id}", response_model=LeaveRequestDetail)
def get_leave_request_details(
    leave_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get details of a specific leave request by ID.
    """
    return leave_crud.get_leave_request_by_id(db, leave_request_id)



