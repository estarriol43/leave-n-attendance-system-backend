from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from ..models.notification import Notification
from ..schemas.notification import NotificationBase, PaginationMeta


def get_user_notifications(
    db: Session,
    user_id: int,
    unread_only: bool = False,
    page: int = 1,
    per_page: int = 10
) -> Dict[str, Any]:
    # Build the base query
    query = db.query(Notification).filter(Notification.user_id == user_id)
    
    # Apply unread filter if specified
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    notifications = query.order_by(Notification.created_at.desc()) \
        .offset((page - 1) * per_page) \
        .limit(per_page) \
        .all()
    
    # Convert to response format
    notification_list = [
        NotificationBase(
            id=notification.id,
            title=notification.title,
            message=notification.message,
            related_to=notification.related_to,
            related_id=notification.related_id,
            is_read=notification.is_read,
            created_at=notification.created_at
        )
        for notification in notifications
    ]
    
    # Calculate pagination metadata
    total_pages = (total + per_page - 1) // per_page
    
    return {
        "notifications": notification_list,
        "pagination": PaginationMeta(
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages
        )
    }
