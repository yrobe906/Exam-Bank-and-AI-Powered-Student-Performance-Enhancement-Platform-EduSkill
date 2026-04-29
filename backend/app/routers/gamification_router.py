import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Form, File, UploadFile, Request
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from app.models.user_models import User
from app.schemas.gamification_schemas import (
    GamificationProfile, LeaderboardResponse, GamificationSummary, XPTransactionList,
    AdminAllRequestsResponse, GamificationSidebar
)
from app.schemas.unlock_schemas import UnlockRequestOut
from app.services.gamification_service import GamificationService, get_gamification_service
from app.utils.gamification_utils import get_tier
from app.models.gamification_models import GamificationActivityModel
from auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="",
    tags=["Gamification"]
)

@router.get("/profile", response_model=GamificationProfile)
def get_gamification_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user gamification profile (XP, tier, streak, badges)."""
    service = get_gamification_service(db)
    return service.get_profile(current_user.id)

@router.get("/profile/public")
def get_gamification_profile_public(
    user_id: int = 1,  # Default to first user for testing
    db: Session = Depends(get_db)
):
    """Get user gamification profile without authentication (for testing)."""
    service = get_gamification_service(db)
    return service.get_profile(user_id)

@router.get("/sidebar")
def get_gamification_sidebar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user gamification data for sidebar display."""
    service = get_gamification_service(db)
    return service.get_sidebar(current_user.id)

@router.get("/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(
    subject: Optional[str] = Query(None, description="Filter by subject for teacher view"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get gamification leaderboard (premium page feature)."""
    service = get_gamification_service(db)
    return service.get_leaderboard(subject, page, limit)

@router.post("/award-exam-submission/{exam_id}")
def award_exam_submission(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Award XP for exam submission (called from exam_router)."""
    service = get_gamification_service(db)
    xp = service.award_exam_submission_xp(current_user.id, exam_id)
    if xp is None:
        raise HTTPException(status_code=400, detail="On cooldown")
    return {"xp_awarded": xp}

@router.post("/award-exam-result/{exam_id}")
def award_exam_result(
    exam_id: int,
    percentage: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Award XP for exam result."""
    service = get_gamification_service(db)
    xp = service.award_exam_result_xp(current_user.id, exam_id, percentage)
    return {"xp_awarded": xp}

@router.post("/award-premium-purchase/{content_id}")
def award_premium_purchase(
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Award XP for premium content purchase."""
    service = get_gamification_service(db)
    xp = service.award_premium_purchase_xp(current_user.id, content_id)
    return {"xp_awarded": xp}

@router.post("/daily-login")
def daily_login(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Daily login XP + streak."""
    service = get_gamification_service(db)
    xp = service.award_daily_login_xp(current_user.id)
    return {"xp_awarded": xp, "message": "Daily streak continued!" if xp > 0 else "Already logged today"}

@router.post("/unlock/request/with-payment", response_model=UnlockRequestOut)
async def submit_unlock_request_with_payment(
    request: Request,
    content_id: int = Form(...),
    content_type: str = Form("mock_exam"),
    content_title: str = Form("Premium Mock Exam"),
    unlock_method: str = Form(...),
    payment_method: Optional[str] = Form(None),
    payment_proof: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit unlock request with payment proof file upload (mock_exam focus)."""
    if payment_proof is None:
        form = await request.form()
        alt_payment = form.get("paymentProofFile") or form.get("paymentProof") or form.get("proof")
        if isinstance(alt_payment, UploadFile):
            payment_proof = alt_payment
            logger.info(f"Received payment proof via alternate form field: {alt_payment.filename}")
    from app.crud.unlock_crud_fixed import create_unlock_request, calculate_xp_required
    from app.models.exam_models import ExamModel
    from app.models.admin import AdminUnlockRequest

    # Get exam (content_id = exam_id for mock_exam)
    exam = db.query(ExamModel).filter(ExamModel.id == content_id).first()
    if not exam or exam.pricing_type != "Premium":
        raise HTTPException(status_code=400, detail="Premium exam not found")

    from app.crud.unlock_crud_fixed import pay_with_points

    points_req = calculate_xp_required(exam.amount)
    
    if unlock_method == "points":
        # Deduct points IMMEDIATELY on submission, create pending request for admin approval
        unlock_record = pay_with_points(db, current_user.id, content_id, points_req)
        unlock_method_flag = "points_deducted"
    else:
        unlock_method_flag = unlock_method
        
    # Create pending request for history/admin review (points already deducted if points method)
    request = create_unlock_request(
        db, current_user.id, content_id, unlock_method_flag,
        payment_method, payment_proof, points_req, exam.amount
    )
    
    # Also create AdminUnlockRequest for admin review
    admin_request = AdminUnlockRequest(
        user_id=current_user.id,
        username=current_user.username,
        full_name=current_user.full_name,
        email=current_user.email,
        user_xp=current_user.xp_points or 0,
        user_tier=current_user.current_tier or "bronze",
        user_streak=0,  # TODO: calculate from gamification data
        content_type=content_type,
        content_id=content_id,
        content_title=content_title,
        unlock_method=unlock_method,
        points_used=points_req if unlock_method == "points" else 0,
        price=exam.amount if exam else 0.0,
        payment_method=payment_method,
        transaction_ref=None,  # TODO: add transaction ref support
        request_reason=f"Unlock request for {content_title} via {unlock_method}",
        payment_proof_path=request.payment_proof_path
    )
    db.add(admin_request)
    db.commit()
    
    return request

@router.post("/unlock/direct/{content_type}/{content_id}")
def unlock_content_direct(
    content_type: str,
    content_id: int,
    payment_proof: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Direct unlock when payment is confirmed."""
    
    # Validate content exists and is premium
    if content_type == "resource":
        from app.models.resource_models import Resource
        content = db.query(Resource).filter(Resource.id == content_id).first()
        is_premium = getattr(content, 'is_premium', False)
    elif content_type == "exam":
        from app.models.exam_models import ExamModel
        content = db.query(ExamModel).filter(ExamModel.id == content_id).first()
        is_premium = getattr(content, 'pricing_type', 'Free') == 'Premium'
    else:
        raise HTTPException(status_code=400, detail="Invalid content type")
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if not is_premium:
        raise HTTPException(status_code=400, detail="Content is not premium")
    
    # Handle payment proof if provided
    payment_proof_path = None
    if payment_proof:
        from pathlib import Path
        UPLOAD_DIR = Path("payment_proof")
        UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
        from datetime import datetime
        filename = f"proof_{current_user.id}_{content_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{payment_proof.filename}"
        path = UPLOAD_DIR / filename
        with open(path, "wb") as f:
            f.write(payment_proof.file.read())
        payment_proof_path = f"/payment_proof/{filename}"
        
        # Create AdminUnlockRequest for admin review
        from app.models.admin import AdminUnlockRequest
        admin_request = AdminUnlockRequest(
            user_id=current_user.id,
            username=current_user.username,
            full_name=current_user.full_name,
            email=current_user.email,
            user_xp=current_user.xp_points or 0,
            user_tier=current_user.current_tier or "bronze",
            user_streak=0,  # TODO: calculate from gamification data
            content_type=content_type,
            content_id=content_id,
            content_title=content.title if hasattr(content, 'title') else content.name,
            unlock_method="payment",
            points_used=0,
            price=0.0,  # TODO: get actual price
            payment_method="bank_transfer",
            transaction_ref=None,
            request_reason=f"Direct unlock with payment proof for {content_type} {content_id}",
            payment_proof_path=payment_proof_path
        )
        db.add(admin_request)
    
    # Check if user already has access
    from app.models.admin import UserPremiumAccess
    existing_access = db.query(UserPremiumAccess).filter(
        UserPremiumAccess.user_id == current_user.id,
        UserPremiumAccess.content_type == content_type,
        UserPremiumAccess.content_id == content_id
    ).first()
    
    if existing_access:
        raise HTTPException(status_code=400, detail="You already have access to this content")
    
    # Grant access
    access = UserPremiumAccess(
        user_id=current_user.id,
        content_type=content_type,
        content_id=content_id,
        payment_method="direct_payment"
    )
    
    db.add(access)
    
    # Award XP for premium purchase
    service = get_gamification_service(db)
    xp_awarded = service.award_premium_purchase_xp(current_user.id, content_id)
    
    db.commit()
    
    return {
        "message": "Content unlocked successfully", 
        "xp_awarded": xp_awarded,
        "access_id": access.id
    }

@router.get("/unlock/check-access/{content_type}/{content_id}")
def check_premium_access(
    content_type: str,
    content_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user has access to premium content."""
    
    from app.models.admin import UserPremiumAccess
    access = db.query(UserPremiumAccess).filter(
        UserPremiumAccess.user_id == current_user.id,
        UserPremiumAccess.content_type == content_type,
        UserPremiumAccess.content_id == content_id
    ).first()
    
    return {"has_access": access is not None}

@router.get("/summary", response_model=GamificationSummary)
def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user gamification summary (badges, activities)."""
    service = get_gamification_service(db)
    return service.get_summary(current_user.id)

@router.get("/transactions", response_model=XPTransactionList)
def get_transactions(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent XP transactions."""
    service = get_gamification_service(db)
    return service.get_transactions(current_user.id, limit)



@router.get("/debug/{user_id}/xp-history")
def get_xp_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """DEBUG: Get XP history and total from activities + user XP."""
    activities = db.query(GamificationActivityModel).filter(
        GamificationActivityModel.user_id == user_id
    ).order_by(GamificationActivityModel.created_at.desc()).limit(50).all()
    
    user = db.query(User).filter(User.id == user_id).first()
    
    history = [{
        "id": a.id,
        "activity_type": a.activity_type,
        "content_id": a.content_id,
        "xp_awarded": a.xp_awarded,
        "created_at": a.created_at.isoformat()
    } for a in activities]
    
    total_awarded = sum(a.xp_awarded for a in activities)
    
    return {
        "user_id": user_id,
        "current_xp": user.xp_points if user else 0,
        "total_awarded_from_activities": total_awarded,
        "activities": history[:20],
        "cooldowns_active": len([a for a in activities if a.is_cooldown_active])
    }

# Admin endpoints for managing premium unlock requests

@router.get("/admin/unlock-requests")
def get_unlock_requests(
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all unlock requests for admin review."""
    from app.models.admin import AdminUnlockRequest
    from app.schemas.admin_schemas import AdminUnlockRequestResponse
    
    query = db.query(AdminUnlockRequest)
    if status:
        query = query.filter(AdminUnlockRequest.status == status)
    
    requests = query.order_by(AdminUnlockRequest.created_at.desc()).all()
    return [AdminUnlockRequestResponse.from_orm(request) for request in requests]

@router.patch("/admin/unlock-request/{request_id}")
def process_unlock_request(
    request_id: int,
    update_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve or reject an unlock request."""
    from app.models.admin import AdminUnlockRequest, UserPremiumAccess
    
    request = db.query(AdminUnlockRequest).filter(AdminUnlockRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Request has already been processed")
    
    status = update_data.get("status")
    admin_notes = update_data.get("admin_notes")
    
    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    request.status = status
    request.admin_notes = admin_notes
    request.processed_at = db.func.now()
    request.processed_by = current_user.id
    
    # If approved, grant access
    if status == "approved":
        access = UserPremiumAccess(
            user_id=request.user_id,
            content_type=request.content_type,
            content_id=request.content_id,
            granted_by=current_user.id,
            payment_method="admin_approval"
        )
        db.add(access)
        
        # Award XP for premium purchase
        service = get_gamification_service(db)
        service.award_premium_purchase_xp(request.user_id, request.content_id)
    
    db.commit()
    
    return {"message": f"Request {status} successfully"}

