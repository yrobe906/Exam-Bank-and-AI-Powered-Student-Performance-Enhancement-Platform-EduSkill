from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, case
from fastapi import HTTPException, UploadFile, File
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)

from ..models.unlock_models_fixed import UnlockRequestModel, StudentExamUnlockModel
from ..models.user_models import User
from ..models.exam_models import ExamModel
from ..models.gamification_models import GamificationActivityModel
from ..schemas.unlock_schemas import *


UPLOAD_DIR = Path("payment_proof")
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

def create_unlock_request(
    db: Session,
    user_id: int,
    exam_id: int,
    unlock_method: str,
    section_id: Optional[int] = None,
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
    if section_id is not None and isinstance(section_id, int):
        existing = db.query(UnlockRequestModel).filter(
            UnlockRequestModel.user_id == user_id,
            UnlockRequestModel.exam_id == exam_id,
            UnlockRequestModel.section_id == section_id,
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

    logger.info(f"create_unlock_request params: exam_id={exam_id}, unlock_method='{unlock_method}', section_id={repr(section_id)}, payment_method={repr(payment_method)}, payment_proof={getattr(payment_proof, 'filename', type(payment_proof).__name__ if payment_proof else None)}")
    
    # Clean payment handling
    real_payment_method = payment_method.strip() if isinstance(payment_method, str) and payment_method and payment_method.strip() else None
    real_payment_proof = None
    if isinstance(payment_proof, UploadFile):
        real_payment_proof = payment_proof
    elif hasattr(payment_proof, 'filename') and hasattr(payment_proof, 'file'):
        real_payment_proof = payment_proof
    
    try:
        real_section_id = int(section_id) if section_id is not None else None
    except (ValueError, TypeError):
        logger.warning(f"Invalid section_id '{repr(section_id)}', treating as None")
        real_section_id = None

    # Validate unlock_method
    if not isinstance(unlock_method, str) or not unlock_method.strip():
        logger.warning(f"Invalid unlock_method '{repr(unlock_method)}', defaulting to 'request'")
        unlock_method = 'request'
    else:
        unlock_method = unlock_method.strip()
    
    payment_proof_path = None
    if real_payment_proof:  # Save payment proof if uploaded
        logger.info(f"Saving payment proof: {real_payment_proof.filename}")
        if not real_payment_proof.content_type.startswith('image/'):
            raise HTTPException(400, "Only image formats (JPEG, PNG, WEBP, GIF) allowed")
        filename = f"proof_{user_id}_{exam_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{real_payment_proof.filename}"
        path = UPLOAD_DIR / filename
        with open(path, "wb") as f:
            f.write(real_payment_proof.file.read())
        payment_proof_path = f"/payment_proof/{filename}"
    elif real_payment_proof:
        logger.warning(f"Payment proof provided but no payment_method (points?): {real_payment_proof.filename}")
    else:
        logger.info(f"No payment proof needed for unlock_method='{unlock_method}', payment_method={real_payment_method}")

    request = UnlockRequestModel(
        user_id=user_id,
        exam_id=exam_id,
        section_id=real_section_id,
        content_id=exam_id if real_section_id is None else exam_id,  # use exam_id for whole exam
        content_type='mock_exam',
        exam_name=exam.name,
        unlock_method=unlock_method,
        points_required=points_required,
        price=price,
        payment_method=real_payment_method,
        payment_proof_path=payment_proof_path,
        status="pending"
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    if request.unlock_method is None:
        logger.error(f"CRITICAL: unlock_method None after persist for new request!")
        db.rollback()
        raise ValueError("unlock_method failed to persist")
    logger.info(f"Successfully created unlock request {request.id} with method '{request.unlock_method}'")
    return request

def pay_with_points(
    db: Session,
    user_id: int,
    exam_id: int,
    points_required: Optional[int] = None,
    section_id: Optional[int] = None
) -> UnlockRequestModel:
    """**IMMEDIATE XP deduction + pending request** (like payment flow)"""
    points_required = int(points_required or 0)
    logger.info(f"pay_with_points IMMEDIATE: user={user_id}, exam={exam_id}, points={points_required}")
    
    # Get user + exam
    user = db.query(User).filter(User.id == user_id).first()
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    
    if not user:
        raise HTTPException(404, "User not found")
    if not exam:
        logger.error("pay_with_points: Exam not found")
        raise HTTPException(404, "Exam not found")
    if exam.pricing_type != "Premium":
        logger.error("pay_with_points: Exam not premium")
        raise HTTPException(400, "Exam is not premium")
    
    # **1. CHECK & IMMEDIATELY DEDUCT XP**
    if user.xp_points < points_required:
        logger.warning(f"Insufficient XP: user {user_id} has {user.xp_points}, needs {points_required}")
        raise HTTPException(400, f"Insufficient XP points: need {points_required}, have {user.xp_points}")
    
    user.xp_points -= points_required
    logger.info(f"✅ XP deducted: user {user_id} {points_required}XP → {user.xp_points} remaining")
    
    # Log activity
    from ..models.gamification_models import GamificationActivityModel
    activity = GamificationActivityModel(
        user_id=user_id,
        activity_type='points_redemption',
        content_id=exam_id,
        content_type='exam_unlock_request',
        xp_awarded=-points_required
    )
    db.add(activity)
    
    # **2. Create pending request (like payment flow)**
    try:
        request = create_unlock_request(
            db, user_id, exam_id, 'points', 
            section_id=section_id,
            payment_method=None, payment_proof=None,
            points_required=points_required, price=exam.amount
        )
        # **3. Track deducted points**
        request.points_used = points_required  # For refund on reject
        
        db.commit()
        db.refresh(request)
        logger.info(f"✅ Points request CREATED: ID={request.id}, points_used={request.points_used}")
        return request
        
    except Exception as e:
        # **CRITICAL**: Rollback XP deduction on error
        logger.error(f"pay_with_points ERROR - REFUNDING XP: {str(e)}", exc_info=True)
        user.xp_points += points_required  # Refund
        db.rollback()
        if hasattr(e, 'status_code'):
            raise
        raise HTTPException(500, f"Failed to create points request: {str(e)}")

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
            unlock_method=r.unlock_method or "unknown", points_required=r.points_required, price=r.price,
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
    if not action or action not in ["approve", "reject"]:
        logger.error(f"Invalid action '{action}' for request {request_id}")
        raise HTTPException(400, f"Invalid action: must be 'approve' or 'reject'")
    logger.info(f"Processing unlock request ID={request_id}, action={action}, method={method}")
    request = get_unlock_request(db, request_id)
    logger.info(f"Request status: {request.status}, unlock_method: {request.unlock_method}, pricing_type: {request.pricing_type}")
    if request.status != "pending":
        raise HTTPException(400, f"Only pending requests can be processed. Current status: {request.status}")

    if action == "reject":
        # **REFUND XP for points redemption**
        if request.unlock_method == 'points' and getattr(request, 'points_used', 0) > 0:
            user = db.query(User).filter(User.id == request.user_id).first()
            if user:
                refunded = request.points_used
                user.xp_points += refunded
                logger.info(f"💸 REFUNDED {refunded}XP to user {request.user_id} (reject {request.id})")
                
                # Log refund activity
                activity = GamificationActivityModel(
                    user_id=request.user_id,
                    activity_type='points_refund_reject',
                    content_id=request.exam_id,
                    content_type='exam_unlock_reject',
                    xp_awarded=refunded
                )
                db.add(activity)
        
        request.status = "rejected"
        request.pricing_type = 'free'
    elif action == "approve":
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(404, "User not found")
        
        points_deducted = 0
        do_points_deduct = method == "points"
        if do_points_deduct:
            logger.info(f"XP check for admin points approval: user {user.id} has {user.xp_points}, required {request.points_required}")
            points_deducted = min(user.xp_points, request.points_required)  # Deduct available XP, even if less
            user.xp_points -= points_deducted
            
            # Log XP deduction
            activity = GamificationActivityModel(
                user_id=user.id,
                activity_type='exam_unlock_deduct',
                content_id=request.exam_id,
                content_type='exam',
                xp_awarded=-points_deducted
            )
            db.add(activity)
        else:
            logger.info(f"Skipping XP deduction - using {method or request.unlock_method} method")
        
        logger.info(f"Exam validation: exam_id={request.exam_id}, exam_name='{request.exam_name}'")
        # Validate/recover exam_id with clear error
        if request.exam_id is None:
            if request.exam_name:
                logger.warning(f"Request ID {request_id} missing exam_id, recovering from exam_name '{request.exam_name}'")
                exam = db.query(ExamModel).filter(ExamModel.name == request.exam_name).first()
                if exam:
                    request.exam_id = exam.id
                    logger.info(f"Recovered exam_id={exam.id} from name")
                else:
                    raise HTTPException(400, f"Exam not found by name '{request.exam_name}' for request {request_id}. Check exam data.")
            else:
                raise HTTPException(400, f"Request {request_id} missing exam_id AND exam_name. Cannot process.")
        
        # Verify exam exists and is premium
        exam = db.query(ExamModel).filter(ExamModel.id == request.exam_id).first()
        logger.info(f"Exam lookup result: exists={exam is not None}, pricing_type={getattr(exam, 'pricing_type', 'N/A')}")
        if not exam:
            raise HTTPException(404, f"Exam ID {request.exam_id} not found for request {request_id}")
        if exam.pricing_type != "Premium":
            raise HTTPException(400, f"Exam {request.exam_id} is not premium content")

        
# Always ensure StudentExamUnlockModel exists for approved requests
        unlock_filter = and_(
            StudentExamUnlockModel.user_id == request.user_id,
            StudentExamUnlockModel.exam_id == request.exam_id
        )
        if request.section_id is not None:
            unlock_filter = and_(unlock_filter, StudentExamUnlockModel.section_id == request.section_id)
        else:
            unlock_filter = and_(unlock_filter, StudentExamUnlockModel.section_id.is_(None))

        existing_unlock = db.query(StudentExamUnlockModel.id).filter(unlock_filter).scalar() is not None
        if existing_unlock:
            existing_unlock_record = db.query(StudentExamUnlockModel).filter(
                StudentExamUnlockModel.user_id == request.user_id,
                StudentExamUnlockModel.exam_id == request.exam_id,
                StudentExamUnlockModel.section_id == request.section_id if request.section_id else None
            ).first()
        else:
            existing_unlock_record = None

        unlock_method = request.unlock_method if request.unlock_method != 'request' else 'admin_approved'
        if existing_unlock_record:
            # Update existing
            existing_unlock_record.unlock_method = unlock_method
            existing_unlock_record.points_used = points_deducted
            existing_unlock_record.payment_proof = request.payment_proof_path
            existing_unlock_record.pricing_type = 'free'
            existing_unlock_record.unlocked_at = datetime.utcnow()
        else:
            unlock = StudentExamUnlockModel(
                user_id=request.user_id,
                exam_id=request.exam_id,
                section_id=request.section_id,
                unlock_method=unlock_method,
                points_used=points_deducted,
                payment_proof=request.payment_proof_path,
                pricing_type='free',
                unlocked_at=datetime.utcnow()
            )
            db.add(unlock)

        request.status = "approved"
        request.payment_verified = True
        request.pricing_type = 'free'
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
    Hard delete unlock request/transaction from database as per user requirement.
    """
    request = get_unlock_request(db, request_id)
    
    # Delete related StudentExamUnlockModel if exists
    db.query(StudentExamUnlockModel).filter(
        StudentExamUnlockModel.user_id == request.user_id,
        StudentExamUnlockModel.exam_id == request.exam_id,
        StudentExamUnlockModel.section_id == request.section_id
    ).delete(synchronize_session=False)
    
    db.delete(request)
    db.commit()
    return {"deleted": True, "request_id": request_id}

def student_has_exam_access(db: Session, user_id: int, exam_id: int, section_id: Optional[int] = None) -> bool:
    # Check approved request OR unlock record OR free exam
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not exam or exam.pricing_type == "Free":
        return True
    
    # Check StudentExamUnlockModel
    unlock_filter = and_(
        StudentExamUnlockModel.user_id == user_id,
        StudentExamUnlockModel.exam_id == exam_id
    )
    if section_id is not None:
        unlock_filter = and_(unlock_filter, StudentExamUnlockModel.section_id == section_id)
    else:
        unlock_filter = and_(unlock_filter, StudentExamUnlockModel.section_id.is_(None))

    unlock_exists = db.query(StudentExamUnlockModel.id).filter(unlock_filter).first() is not None
    
    # OR approved UnlockRequestModel
    request_filter = and_(
        UnlockRequestModel.user_id == user_id,
        UnlockRequestModel.exam_id == exam_id,
        UnlockRequestModel.status == "approved"
    )
    if section_id is not None:
        request_filter = and_(request_filter, UnlockRequestModel.section_id == section_id)
    else:
        request_filter = and_(request_filter, UnlockRequestModel.section_id.is_(None))

    approved_request = db.query(UnlockRequestModel.id).filter(request_filter).first() is not None
    
    return unlock_exists or approved_request

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

