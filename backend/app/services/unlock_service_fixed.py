from typing import Optional
from fastapi import UploadFile
from datetime import datetime

from sqlalchemy.orm import Session
from ..crud.unlock_crud_fixed import (
    create_unlock_request, pay_with_points, get_my_unlock_requests, get_admin_unlock_requests,
    process_unlock_request, verify_payment, student_has_exam_access, calculate_xp_required
)
from app.utils.gamification_utils import get_tier
from ..models.exam_models import ExamModel
from ..models.user_models import User
from ..schemas.unlock_schemas import XPResponse, HasAccessResponse


def service_create_unlock_request(
    db: Session,
    user_id: int,
    exam_id: int,
    unlock_method: str,
    section_id: Optional[int] = None,
    payment_method: Optional[str] = None,
    payment_proof: Optional[UploadFile] = None
):
    # Get exam for price/points
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not exam or exam.pricing_type != "Premium":
        raise ValueError("Invalid premium exam")
    
    points_req = calculate_xp_required(exam.amount)
    request = create_unlock_request(
        db, user_id, exam_id, section_id, unlock_method,
        payment_method, payment_proof, points_req, exam.amount
    )
    return request

def service_pay_with_points(
    db: Session,
    user_id: int,
    exam_id: int,
    section_id: Optional[int] = None
):
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not exam or exam.pricing_type != "Premium":
        raise ValueError("Invalid premium exam")
    
    points_req = calculate_xp_required(exam.amount)
    unlock = pay_with_points(db, user_id, exam_id, section_id, points_req)
    return unlock

def service_get_my_requests(db: Session, user_id: int, status: Optional[str] = None):
    return get_my_unlock_requests(db, user_id, status)

def service_get_admin_requests(db: Session, status: Optional[str] = None, limit: int = 100):
    return get_admin_unlock_requests(db, status, limit)

def service_process_request(
    db: Session,
    request_id: int,
    action: str,
    method: Optional[str] = None,
    transaction_ref: Optional[str] = None,
    admin_notes: Optional[str] = None
):
    processed = process_unlock_request(db, request_id, action, method, transaction_ref, admin_notes)
    
    # GUARANTEE StudentExamUnlockModel for approved (fixes AvailableTests access)
    if processed.status == 'approved' and processed.exam_id:
        from app.models.unlock_models_fixed import StudentExamUnlockModel
        
        # Force create/update unlock record
        unlock = db.query(StudentExamUnlockModel).filter(
            StudentExamUnlockModel.user_id == processed.user_id,
            StudentExamUnlockModel.exam_id == processed.exam_id
        ).first()
        points_used = processed.points_required or 0
        if not unlock:
            unlock = StudentExamUnlockModel(
                user_id=processed.user_id,
                exam_id=processed.exam_id,
                unlock_method='admin_approved',
                points_used=points_used,
                unlocked_at=datetime.utcnow()
            )
            db.add(unlock)
        else:
            unlock.unlock_method = 'admin_approved'
            unlock.points_used = points_used
            unlock.unlocked_at = datetime.utcnow()
        
        user = db.query(User).filter(User.id == processed.user_id).first()
        if user:
            user.current_tier = get_tier(user.xp_points)
        db.commit()
        print(f'ENSURED unlock for user={processed.user_id}, exam={processed.exam_id}')
    
    return processed

def service_verify_payment(db: Session, request_id: int, verified: bool, transaction_ref: Optional[str] = None):
    return verify_payment(db, request_id, verified, transaction_ref)

def service_delete_unlock_request(db: Session, request_id: int):
    """Delete unlock request (soft delete)"""
    from app.crud.unlock_crud_fixed import delete_unlock_request
    return delete_unlock_request(db, request_id)

def service_check_eligibility(db: Session, user_id: int, exam_id: int) -> XPResponse:
    user = db.query(User).filter(User.id == user_id).first()
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not user or not exam:
        return XPResponse(can_unlock=False, xp_required=0, user_xp=0, reason="Invalid user/exam")
    
    if exam.pricing_type != "Premium":
        return XPResponse(can_unlock=True, xp_required=0, user_xp=user.xp_points, reason="Free exam")
    
    points_req = calculate_xp_required(exam.amount)
    can = user.xp_points >= points_req
    shortage = points_req - user.xp_points if not can else 0
    return XPResponse(
        xp_required=points_req, can_unlock=can, user_xp=user.xp_points,
        shortage=shortage if shortage > 0 else None,
        reason="Insufficient XP" if not can else None
    )

def service_has_exam_access(db: Session, user_id: int, exam_id: int, section_id: Optional[int] = None) -> HasAccessResponse:
    has = student_has_exam_access(db, user_id, exam_id, section_id)
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    is_prem = exam.pricing_type == "Premium" if exam else False
    method_used = "unlock" if has and is_prem else None
    return HasAccessResponse(has_access=has, is_premium=is_prem, unlock_method_used=method_used)

