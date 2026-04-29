from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from app.auth import get_current_user  # Assume exists from auth.py
from app.models.user_models import User
from app.schemas.unlock_schemas import *
from app.services.unlock_service_fixed import *
from app.models.unlock_models_fixed import StudentExamUnlockModel
from app.crud.unlock_crud_fixed import pay_with_points

router = APIRouter(prefix="/unlock", tags=["Unlock Requests"])

@router.post("/requests", response_model=UnlockRequestOut)
def create_request(
    exam_id: int = Form(...),
    unlock_method: str = Form(...),
    payment_method: Optional[str] = Form(None),
    payment_proof: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Student creates unlock request"""
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
    from app.crud.unlock_crud_fixed import calculate_xp_required
    return {"xp_required": calculate_xp_required(amount)}

