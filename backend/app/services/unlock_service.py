from typing import Optional
from fastapi import HTTPException

from sqlalchemy.orm import Session
from ..crud.unlock_crud_fixed import (
    create_unlock_request, get_my_unlock_requests, get_admin_unlock_requests,
    process_unlock_request, verify_payment, student_has_exam_access, calculate_xp_required, delete_unlock_request
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
    payment_method: Optional[str] = None,
    payment_proof: Optional['UploadFile'] = None
):
    # Get exam for price/points
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not exam or exam.pricing_type != "Premium":
        raise ValueError("Invalid premium exam")
    
    points_req = calculate_xp_required(exam.amount)
    request = create_unlock_request(
        db, user_id, exam_id, unlock_method, section_id=None,
        payment_method=payment_method, payment_proof=payment_proof,
        points_required=points_req, price=exam.amount
    )
    
    # Also create AdminUnlockRequest for admin review
    from ..models.admin import AdminUnlockRequest
    from ..models.user_models import User
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        admin_request = AdminUnlockRequest(
            user_id=user_id,
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            user_xp=user.xp_points or 0,
            user_tier=user.current_tier or "bronze",
            user_streak=0,  # TODO: calculate from gamification data
            content_type='mock_exam',
            content_id=exam_id,
            content_title=exam.name,
            unlock_method=unlock_method,
            points_used=points_req if unlock_method == "points" else 0,
            price=exam.amount,
            payment_method=payment_method,
            transaction_ref=None,
            request_reason=f"Unlock request for {exam.name} via {unlock_method}",
            payment_proof_path=request.payment_proof_path
        )
        db.add(admin_request)
        db.commit()
    
    return request

def service_cancel_unlock_request(db: Session, request_id: int):
    """Cancel pending unlock request"""
    from ..crud.unlock_crud_fixed import get_unlock_request_by_id
    request = get_unlock_request_by_id(db, request_id)
    if not request or request.status != 'pending':
        raise ValueError("Cannot cancel non-pending request")
    
    request.status = 'cancelled'
    db.commit()
    return request

def service_get_unlock_request_by_id(db: Session, request_id: int):
    from ..crud.unlock_crud_fixed import get_unlock_request_by_id
    return get_unlock_request_by_id(db, request_id)

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
    try:
        processed = process_unlock_request(db, request_id, action, method, transaction_ref, admin_notes)

        user = db.query(User).filter(User.id == processed.user_id).first()
        if user:
            user.current_tier = get_tier(user.xp_points)
            db.commit()
        return processed
    except HTTPException:
        raise  # Re-raise FastAPI exceptions
    except Exception as e:
        logger.error(f"Service error processing unlock request {request_id}: {str(e)}", exc_info=True)
        raise HTTPException(500, f"Internal error processing request: {str(e)}")

def service_verify_payment(db: Session, request_id: int, verified: bool, transaction_ref: Optional[str] = None):
    return verify_payment(db, request_id, verified, transaction_ref)

def service_delete_unlock_request(db: Session, request_id: int):
    """
    Hard delete unlock request/transaction from database
    """
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

def service_has_exam_access(db: Session, user_id: int, exam_id: int) -> HasAccessResponse:
    has = student_has_exam_access(db, user_id, exam_id)
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    is_prem = exam.pricing_type == "Premium" if exam else False
    method_used = "unlock" if has and is_prem else None
    return HasAccessResponse(has_access=has, is_premium=is_prem, unlock_method_used=method_used)
