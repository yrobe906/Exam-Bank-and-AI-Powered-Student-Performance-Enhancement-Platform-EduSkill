from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime
from ..models.user_models import User

# Base editable fields (common to all roles)
class UserEditBase(BaseModel):
    full_name: str
    gender: Literal["male", "female"]

# Role-specific edit schemas
class UserEditStudent(UserEditBase):
    school_id: Optional[str] = None
    grade: Optional[int] = None

class UserEditTeacher(UserEditBase):
    phone: Optional[str] = None
    school_name: Optional[str] = None
    subject_assigned: Optional[str] = None
    teaching_grade: Optional[int] = None

class UserEditEduoffice(UserEditBase):
    woreda: Optional[str] = None
    school_supervising: Optional[str] = None

# Union type for all edits (router will validate based on role)
class UserEditRequest(BaseModel):
    role: Literal["student", "teacher", "eduoffice"]
    data: dict  # Will contain role-specific fields

# Response schema (hide sensitive fields)
class UserEditResponse(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    role: str
    gender: str
    school_id: Optional[str] = None
    grade: Optional[int] = None
    phone: Optional[str] = None
    school_name: Optional[str] = None
    subject_assigned: Optional[str] = None
    teaching_grade: Optional[int] = None
    woreda: Optional[str] = None
    school_supervising: Optional[str] = None
    profile_photo: Optional[str] = None
    status: str
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # For SQLAlchemy ORM compatibility

