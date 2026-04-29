from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class AdminBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminResponse(AdminBase):
    id: int
    is_active: bool
    created_at: datetime
    role: str = "admin"
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: AdminResponse


class AdminUnlockRequestBase(BaseModel):
    content_type: str
    content_id: int
    content_title: str
    unlock_method: str
    points_used: int = 0
    price: float = 0.0
    payment_method: Optional[str] = None
    transaction_ref: Optional[str] = None
    request_reason: Optional[str] = None
    payment_proof_path: Optional[str] = None

class AdminUnlockRequestCreate(AdminUnlockRequestBase):
    pass

class AdminUnlockRequestResponse(AdminUnlockRequestBase):
    id: int
    user_id: int
    username: str
    full_name: str
    email: str
    user_xp: int
    user_tier: str
    user_streak: int
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    processed_by: Optional[int] = None
    
    class Config:
        orm_mode = True

class AdminUnlockRequestUpdate(BaseModel):
    status: str  # 'approved', 'rejected'
    admin_notes: Optional[str] = None


class UserPremiumAccessBase(BaseModel):
    content_type: str
    content_id: int
    payment_method: Optional[str] = None

class UserPremiumAccessResponse(UserPremiumAccessBase):
    id: int
    user_id: int
    access_granted_at: datetime
    granted_by: Optional[int] = None
    
    class Config:
        orm_mode = True