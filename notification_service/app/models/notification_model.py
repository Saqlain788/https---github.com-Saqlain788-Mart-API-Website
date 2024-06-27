# models/notification_model.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    message: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class NotificationCreate(SQLModel):
    user_id: int
    message: str
    status: str

class NotificationUpdate(SQLModel):
    user_id: Optional[int] = None
    message: Optional[str] = None
    status: Optional[str] = None
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
