from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Request
import logging
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from app.auth import get_current_user  # Assume exists from auth.py
from app.models.user_models import User
from app.models.exam_models import ExamModel
from app.schemas.unlock_schemas import *
from app.services.unlock_service import *  # Fixed import
from app.crud.unlock_crud_fixed import pay_with_points, calculate_xp_required, get_unlock_request

router = APIRouter(prefix="/unlock", tags=["Unlock Requests"])

logger = logging.getLogger(__name__)

@router.post("/requests", response_model=UnlockRequestOut)
async def create_request(
    request: Request,
    exam_id: int = Form(...),
    unlock_method: str = Form(...),
    payment_method: Optional[str] = Form(None),
    payment_proof: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"POST /unlock/requests: exam_id={exam_id}, unlock_method='{unlock_method}', payment_method={payment_method}, payment_proof={getattr(payment_proof, 'filename', None)}")
    """Student creates unlock request"""
    # Accept alternate upload field names if frontend sends a different key
    if payment_proof is None:
        form = await request.form()
        alt_payment = form.get("paymentProofFile") or form.get("paymentProof") or form.get("proof")
        if isinstance(alt_payment, UploadFile):
            payment_proof = alt_payment
            logger.info(f"Received payment proof via alternate form field: {alt_payment.filename}")

    from pydantic import ValidationError
    try:
        # Create pydantic model for validation
        req_data = UnlockRequestCreate(
            exam_id=exam_id,
            unlock_method=unlock_method,
            payment_method=payment_method
        )
        processed_request = service_create_unlock_request(
            db, current_user.id, req_data.exam_id, req_data.unlock_method,
            req_data.payment_method, payment_proof
        )
        return processed_request
    except ValidationError as e:
        raise HTTPException(422, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/requests/{request_id}")
def cancel_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Student cancels their own pending unlock request"""
    # Check ownership
    request = service_get_unlock_request_by_id(db, request_id)  # Assume exists
    if not request or request.user_id != current_user.id:
        raise HTTPException(404, "Request not found")
    if request.status != "pending":
        raise HTTPException(400, "Only pending requests can be cancelled")
    
    service_cancel_unlock_request(db, request_id)
    return {"message": "Request cancelled successfully"}

@router.get("/my-requests", response_model=List[UnlockRequestOut])
def get_my_requests(
    status: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service_get_my_requests(db, current_user.id, status)

@router.get("/check-eligibility")
def check_eligibility(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service_check_eligibility(db, current_user.id, exam_id)

@router.get("/has-access")
def has_access(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return service_has_exam_access(db, current_user.id, exam_id)

@router.get("/calculate-xp")
def calc_xp(amount: float = Query(..., ge=0)):
    return {"xp_required": calculate_xp_required(amount)}

@router.post("/pay-points/{exam_id}", response_model=UnlockRequestOut)
def pay_points(
    exam_id: int,
    points_required: Optional[int] = Form(None, description="XP points required from eligibility check"),
    section_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit points redemption request - **IMMEDIATE XP deduction**"""
    if points_required is None or points_required <= 0:
        exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
        if not exam:
            raise HTTPException(404, "Exam not found")
        from app.crud.unlock_crud_fixed import calculate_xp_required
        points_required = calculate_xp_required(exam.amount)
    
    logger.info(f"🔥 Points redemption API: user={current_user.id}, exam={exam_id}, deducting={points_required}XP")
    request = pay_with_points(db, current_user.id, exam_id, points_required, section_id)
    logger.info(f"✅ Request created ID={request.id}, status={request.status}, points_used={getattr(request, 'points_used', 0)}")
    return request
