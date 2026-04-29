from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnnouncementBase(BaseModel):
    title: str
    message: str
    category: str  # academic, achievement
    target_role: str  # student, teacher, both
    is_active: Optional[bool] = True
    file_name: Optional[str] = None


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    category: Optional[str] = None
    target_role: Optional[str] = None
    is_active: Optional[bool] = None
    file_name: Optional[str] = None


class AnnouncementResponse(AnnouncementBase):
    id: int
    created_at: datetime
    file_path: Optional[str] = None

    class Config:
        from_attributes = True