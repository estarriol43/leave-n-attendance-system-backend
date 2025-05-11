from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
import logging
from ..crud import notification as notification_crud
from ..schemas.notification import NotificationListResponse
from ..utils.dependencies import get_current_user
from ..models.user import User
from ..database import get_db

# Get logger
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/notifications",
    tags=["notifications"]
)


@router.get("", response_model=NotificationListResponse)
def get_notifications(
    unread_only: Optional[bool] = Query(False, description="If true, only return unread notifications"),
    page: Optional[int] = Query(1, ge=1, description="Page number"),
    per_page: Optional[int] = Query(10, ge=1, le=100, description="Items per page"),
    request: Request = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get notifications for the current user.
    """
    client_ip = request.client.host
    logger.info(f"User {current_user.email} (ID: {current_user.id}) requesting notifications from {client_ip}")
    
    try:
        # Ensure parameters are valid
        actual_page = max(1, page) if page is not None else 1
        actual_per_page = min(max(1, per_page), 100) if per_page is not None else 10
        
        # Get notifications
        result = notification_crud.get_user_notifications(
            db=db,
            user_id=current_user.id,
            unread_only=unread_only,
            page=actual_page,
            per_page=actual_per_page
        )
        
        logger.info(f"Successfully returned {len(result['notifications'])} notifications for user {current_user.email}")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching notifications")
