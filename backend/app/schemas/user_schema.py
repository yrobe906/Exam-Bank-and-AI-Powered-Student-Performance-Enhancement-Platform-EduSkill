from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


# ---------- Base fields for all users ----------
class UserBase(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    role: Literal["student", "teacher", "eduoffice"]
    gender: Literal["male", "female"]


# ---------- Registration Schema ----------
class UserRegister(UserBase):
    password: str

    # Student
    school_id: Optional[str] = None
    grade: Optional[int] = None

    # Teacher
    phone: Optional[str] = None
    school_name: Optional[str] = None
    subject_assigned: Optional[str] = None
    teaching_grade: Optional[int] = None

    # Edu Office
    woreda: Optional[str] = None
    school_supervising: Optional[str] = None


# ---------- Login Schema ----------
class UserLogin(BaseModel):
    username_or_email: str
    password: str


# ---------- Response Schema (hide password) ----------
class UserResponse(UserBase):
    id: int
    is_approved: bool

    class Config:
        orm_mode = True
