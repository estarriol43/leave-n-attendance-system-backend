from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional
import logging
from ..crud import notification as notification_crud
from ..schemas.notification import NotificationListResponse, NotificationReadResponse, NotificationReadAllResponse
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


@router.patch("/{notification_id}/read", response_model=NotificationReadResponse)
def mark_notification_as_read(
    notification_id: int,
    request: Request = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark a specific notification as read.
    """
    client_ip = request.client.host
    logger.info(f"User {current_user.email} (ID: {current_user.id}) marking notification {notification_id} as read from {client_ip}")
    
    try:
        result = notification_crud.mark_notification_as_read(
            db=db,
            notification_id=notification_id,
            user_id=current_user.id
        )
        logger.info(f"Successfully marked notification {notification_id} as read")
        return result
    except HTTPException as e:
        logger.error(f"HTTP error marking notification as read: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error marking notification as read: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.patch("/read-all", response_model=NotificationReadAllResponse)
def mark_all_notifications_as_read(
    request: Request = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mark all notifications as read for the current user.
    """
    client_ip = request.client.host
    logger.info(f"User {current_user.email} (ID: {current_user.id}) marking all notifications as read from {client_ip}")
    
    try:
        result = notification_crud.mark_all_notifications_as_read(
            db=db,
            user_id=current_user.id
        )
        logger.info(f"Successfully marked {result.count} notifications as read")
        return result
    except Exception as e:
        logger.error(f"Unexpected error marking all notifications as read: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
