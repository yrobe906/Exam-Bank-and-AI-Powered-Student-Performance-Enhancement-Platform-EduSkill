from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .exam_schemas import ExamOut  # Assume exists or create minimal


class UnlockRequestCreate(BaseModel):
    exam_id: int
    section_id: Optional[int] = None
    unlock_method: str  # 'points' or 'payment'
    payment_method: Optional[str] = None  # 'cbe', 'boa', 'telebirr'
    payment_proof: Optional[str] = None  # Handled as UploadFile, store path

class UnlockRequestCreatePayment(UnlockRequestCreate):
    payment_proof: bytes  # Required for payment

class XPResponse(BaseModel):
    xp_required: int
    can_unlock: bool
    user_xp: int
    shortage: Optional[int] = None
    reason: Optional[str] = None

class UnlockRequestOut(BaseModel):
    id: int
    user_id: int
    exam_id: Optional[int] = None
    section_id: Optional[int] = None
    content_id: Optional[int] = None
    exam_name: Optional[str] = None
    unlock_method: Optional[str] = None
    points_required: int
    price: float
    pricing_type: Optional[str] = None
    payment_method: Optional[str]
    payment_proof_path: Optional[str]
    status: str
    payment_verified: bool
    transaction_ref: Optional[str]
    admin_notes: Optional[str]
    created_at: datetime
    reviewed_at: Optional[datetime]

    class Config:
        from_attributes = True

class UnlockRequestAdminOut(UnlockRequestOut):
    user_name: str
    user_email: str
    user_xp: int
    user_tier: str
    user_streak: int  # from gamification
    missing_exam_id: bool = False
    section_id: Optional[int] = None
    pricing_type: Optional[str] = None

class ProcessRequest(BaseModel):
    action: str  # 'approve' or 'reject'
    method: Optional[str] = None  # for approve
    transaction_ref: Optional[str] = None
    admin_notes: Optional[str] = None

class VerifyPayment(BaseModel):
    verified: bool
    transaction_ref: Optional[str] = None

class HasAccessResponse(BaseModel):
    has_access: bool
    is_premium: bool
    unlock_method_used: Optional[str] = None
    section_id: Optional[int] = None

class StudentExamUnlockOut(BaseModel):
    id: int
    user_id: int
    exam_id: int
    section_id: Optional[int] = None
    unlock_method: str
    points_used: int
    pricing_type: Optional[str] = None
    payment_proof_path: Optional[str] = None
    unlocked_at: datetime

    class Config:
        from_attributes = True
