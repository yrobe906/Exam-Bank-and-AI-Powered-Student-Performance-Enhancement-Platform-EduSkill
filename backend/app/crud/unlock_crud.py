from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, case
from fastapi import HTTPException, UploadFile, File
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..models.unlock_models_fixed import UnlockRequestModel, StudentExamUnlockModel
from ..models.user_models import User
from ..models.exam_models import ExamModel
from ..schemas.unlock_schemas import *


UPLOAD_DIR = Path("uploads/payment_proofs")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

def create_unlock_request(
    db: Session,
    user_id: int,
    exam_id: int,
    unlock_method: str,
    payment_method: Optional[str] = None,
    payment_proof: Optional[UploadFile] = None,
    points_required: int = 0,
    price: float = 0.0
) -> UnlockRequestModel:
    # Check if pending request exists
    existing = db.query(UnlockRequestModel).filter(
        UnlockRequestModel.user_id == user_id,
        UnlockRequestModel.exam_id == exam_id,
        UnlockRequestModel.status == "pending"
    ).first()
    if existing:
        raise HTTPException(400, "Pending request already exists")

    # Get exam
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not exam:
        raise HTTPException(404, "Exam not found")
    
    if exam.pricing_type != "Premium":
        raise HTTPException(400, "Exam is not premium")

    payment_proof_path = None
    if payment_proof and unlock_method == "payment":
        if not payment_proof.content_type.startswith(('image/', 'application/pdf')):
            raise HTTPException(400, "Invalid file type")
        filename = f"proof_{user_id}_{exam_id}_{payment_proof.filename}"
        path = UPLOAD_DIR / filename
        with open(path, "wb") as f:
            f.write(payment_proof.file.read())
        payment_proof_path = f"/uploads/payment_proofs/{filename}"

    request = UnlockRequestModel(
        user_id=user_id,
        exam_id=exam_id,
        content_id=exam_id,
        content_type='mock_exam',
        exam_name=exam.name,
        unlock_method=unlock_method,
        points_required=points_required,
        price=price,
        payment_method=payment_method,
        payment_proof_path=payment_proof_path,
        status="pending"
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

def get_my_unlock_requests(db: Session, user_id: int, status: Optional[str] = None) -> List[UnlockRequestOut]:
    query = db.query(UnlockRequestModel).filter(UnlockRequestModel.user_id == user_id)
    if status:
        query = query.filter(UnlockRequestModel.status == status)
    return query.order_by(UnlockRequestModel.created_at.desc()).all()

def get_admin_unlock_requests(db: Session, status: Optional[str] = None, limit: int = 100) -> List[UnlockRequestAdminOut]:
    query = db.query(UnlockRequestModel)
    if status:
        query = query.filter(UnlockRequestModel.status == status)
    requests = query.order_by(
        case((UnlockRequestModel.status == "pending", 1), else_=0).desc(),
        UnlockRequestModel.created_at.desc()
    ).limit(limit).all()
    
    # Enrich with user data
    result = []
    for r in requests:
        user = db.query(User).filter(User.id == r.user_id).first()
        result.append(UnlockRequestAdminOut(
            id=r.id, user_id=r.user_id, exam_id=r.exam_id, exam_name=r.exam_name or "Unknown Exam",
            missing_exam_id=(r.exam_id is None),
            unlock_method=r.unlock_method, points_required=r.points_required, price=r.price,
            payment_method=r.payment_method, payment_proof_path=r.payment_proof_path,
            status=r.status, payment_verified=r.payment_verified, transaction_ref=r.transaction_ref,
            admin_notes=r.admin_notes, created_at=r.created_at, reviewed_at=r.reviewed_at,
            user_name=user.full_name if user else "Unknown",
            user_email=user.email if user else "",
            user_xp=user.xp_points if user else 0,
            user_tier=user.current_tier if user else "bronze",
            user_streak=0  # TODO: from gamification
        ))
    return result

def get_unlock_request(db: Session, request_id: int) -> UnlockRequestModel:
    request = db.query(UnlockRequestModel).filter(UnlockRequestModel.id == request_id).first()
    if not request:
        raise HTTPException(404, "Request not found")
    return request

def process_unlock_request(
    db: Session,
    request_id: int,
    action: str,
    method: Optional[str] = None,
    transaction_ref: Optional[str] = None,
    admin_notes: Optional[str] = None
):
    request = get_unlock_request(db, request_id)
    if request.status != "pending":
        raise HTTPException(400, "Cannot process non-pending request")
    
    if action == "reject":
        request.status = "rejected"
    elif action == "approve":
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(404, "User not found")
        
        if request.unlock_method == "points" or (request.unlock_method == "payment" and method == "points"):
            if user.xp_points < request.points_required:
                raise HTTPException(400, "Insufficient XP points")
            user.xp_points -= request.points_required
        
        # Validate/recover exam_id
        if request.exam_id is None:
            if request.exam_name:
                exam = db.query(ExamModel).filter(ExamModel.name == request.exam_name).first()
                if exam:
                    request.exam_id = exam.id
                else:
                    raise HTTPException(400, f"Cannot find exam '{request.exam_name}'")
            else:
                raise HTTPException(400, "Request missing exam_id and exam_name")
        
        # Verify exam exists
        exam = db.query(ExamModel).filter(ExamModel.id == request.exam_id).first()
        if not exam:
            raise HTTPException(404, f"Exam {request.exam_id} not found")
        
        # Create unlock record
        existing_unlock = db.query(StudentExamUnlockModel).filter(
            StudentExamUnlockModel.user_id == request.user_id,
            StudentExamUnlockModel.exam_id == request.exam_id
        ).first()
        if not existing_unlock:
            unlock = StudentExamUnlockModel(
                user_id=request.user_id,
                exam_id=request.exam_id,
                unlocked_at=datetime.utcnow()
            )
            db.add(unlock)
        
        request.status = "approved"
        request.payment_verified = True
        request.transaction_ref = transaction_ref
        # Update tier (simple logic)
        if user.xp_points < 300:
            user.current_tier = "bronze"
        elif user.xp_points < 600:
            user.current_tier = "silver"
        elif user.xp_points < 3000:
            user.current_tier = "gold"
        else:
            user.current_tier = "diamond"
    
    request.reviewed_at = datetime.utcnow()
    request.admin_notes = admin_notes
    db.commit()
    return request

def verify_payment(db: Session, request_id: int, verified: bool, transaction_ref: Optional[str] = None):
    request = get_unlock_request(db, request_id)
    request.payment_verified = verified
    request.transaction_ref = transaction_ref
    db.commit()
    return request

def delete_unlock_request(db: Session, request_id: int):
    """
    Hard delete unlock request - removes row from database for all statuses.
    """
    request = get_unlock_request(db, request_id)
    # Delete related StudentExamUnlockModel if exists
    db.query(StudentExamUnlockModel).filter(
        StudentExamUnlockModel.user_id == request.user_id,
        StudentExamUnlockModel.exam_id == request.exam_id
    ).delete(synchronize_session=False)
    db.delete(request)
    db.commit()
    return {"message": "Unlock transaction deleted successfully from database"}

def student_has_exam_access(db: Session, user_id: int, exam_id: int) -> bool:
    # Check unlock record OR free exam
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not exam or exam.pricing_type == "Free":
        return True
    
    unlock = db.query(StudentExamUnlockModel).filter(
        StudentExamUnlockModel.user_id == user_id,
        StudentExamUnlockModel.exam_id == exam_id
    ).first()
    return unlock is not None

def calculate_xp_required(amount: float) -> int:
    # Use frontend rates logic - hardcoded
    rates = [
        (50, 150), (100, 200), (150, 350), (200, 400),
        (250, 450), (300, 500), (350, 550), (400, 700), (500, 3000)
    ]
    if amount <= 0:
        return 0
    for etb, xp in rates:
        if amount <= etb:
            return xp
    return 3000  # max

