# app/routers/resource_router.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from database import get_db
from app.models.resource_models import Resource
from app.models.user_models import User
from auth import get_current_user, get_current_admin  # Keep for future use

router = APIRouter(
    prefix="",
    tags=["Resources"]
)

# Directory to save uploaded resources
RESOURCE_UPLOAD_DIR = Path("uploads/resources")
RESOURCE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ✅ Add new resource
@router.post("/")
async def add_resource(
    title: str = Form(...),
    description: str = Form(None),
    type: str = Form(...),
    subject: str = Form(...),
    grade_level: str = Form(...),
    file: UploadFile = File(...),
    is_premium: bool = Form(False),
    price: float = Form(0.0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save file
    file_path = RESOURCE_UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resource = Resource(
        title=title,
        description=description,
        type=type,
        subject=subject,
        grade_level=grade_level,
        file_path=str(file_path),
        file_name=file.filename,
        file_size=file.spool_max_size if hasattr(file, "spool_max_size") else None,
        uploaded_by=current_user.id,
        is_premium=is_premium,
        price=price
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return {"message": "Resource uploaded successfully", "resource_id": resource.id}


# ✅ List all resources
@router.get("/")
def list_resources(db: Session = Depends(get_db)):
    resources = db.query(Resource).filter(Resource.is_active == True).all()
    return resources


# ✅ Get resource by ID
@router.get("/{resource_id}")
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id, Resource.is_active == True).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


# ✅ Update resource
@router.put("/{resource_id}")
async def update_resource(
    resource_id: int,
    title: str = Form(None),
    description: str = Form(None),
    type: str = Form(None),
    subject: str = Form(None),
    grade_level: str = Form(None),
    is_premium: bool = Form(None),
    price: float = Form(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    resource = db.query(Resource).filter(Resource.id == resource_id, Resource.is_active == True).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # Update fields if provided
    if title is not None:
        resource.title = title
    if description is not None:
        resource.description = description
    if type is not None:
        resource.type = type
    if subject is not None:
        resource.subject = subject
    if grade_level is not None:
        resource.grade_level = grade_level
    if is_premium is not None:
        resource.is_premium = is_premium
    if price is not None:
        resource.price = price
    
    # Handle file update if provided
    if file:
        file_path = RESOURCE_UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        resource.file_path = str(file_path)
        resource.file_name = file.filename
        resource.file_size = file.spool_max_size if hasattr(file, "spool_max_size") else None
    
    db.commit()
    db.refresh(resource)
    
    return {"message": "Resource updated successfully", "resource": resource}


# ✅ Delete resource (soft delete)
@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(Resource).filter(Resource.id == resource_id, Resource.is_active == True).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource.is_active = False
    db.commit()
    
    return {"message": "Resource deleted successfully"}
