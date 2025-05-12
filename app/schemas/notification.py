from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class NotificationBase(BaseModel):
    id: int
    title: str
    message: str
    related_to: str
    related_id: int
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginationMeta(BaseModel):
    total: int
    page: int
    per_page: int
    total_pages: int


class NotificationListResponse(BaseModel):
    notifications: List[NotificationBase]
    pagination: PaginationMeta


class NotificationReadResponse(BaseModel):
    id: int
    is_read: bool

    model_config = ConfigDict(from_attributes=True)


class NotificationReadAllResponse(BaseModel):
    message: str
    count: int
