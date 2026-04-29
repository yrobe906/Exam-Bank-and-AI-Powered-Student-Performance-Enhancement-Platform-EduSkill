from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from app.auth import get_current_user
from app.models.user_models import User
from ..schemas.announcement_schemas import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse
from ..crud.announcement_crud import (
    get_announcements, get_announcement_by_id, create_announcement,
    update_announcement, delete_announcement
)
import shutil
from pathlib import Path
import uuid

router = APIRouter()

# Create uploads directory for announcements
UPLOAD_DIR = Path("uploads/announcements")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def check_eduoffice_or_admin(current_user: User):
    """Check if user is eduoffice or admin."""
    if current_user.role not in ["eduoffice", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only eduoffice and admin can manage announcements"
        )


def save_uploaded_file(upload_file: UploadFile) -> str:
    """Save uploaded file and return the file path."""
    if not upload_file.filename:
        return None

    # Generate unique filename
    file_extension = Path(upload_file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIR / unique_filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return f"announcements/{unique_filename}"


@router.post("/", response_model=AnnouncementResponse)
async def create_new_announcement(
    title: str = Form(...),
    message: str = Form(...),
    category: str = Form(...),
    target_role: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_eduoffice_or_admin(current_user)

    # Validate file type if provided
    if file and file.filename:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )

    # Save file if provided
    file_path = None
    file_name = None
    if file and file.filename:
        file_path = save_uploaded_file(file)
        file_name = file.filename

    announcement_data = AnnouncementCreate(
        title=title,
        message=message,
        category=category,
        target_role=target_role,
        file_name=file_name
    )

    return create_announcement(db, announcement_data, file_path)


@router.get("/", response_model=List[AnnouncementResponse])
async def read_announcements(
    role: Optional[str] = Query(None, description="Filter by role: student, teacher, or both"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Allow all authenticated users to view announcements
    return get_announcements(db, role, skip, limit)


@router.put("/{announcement_id}", response_model=AnnouncementResponse)
async def update_existing_announcement(
    announcement_id: int,
    title: Optional[str] = Form(None),
    message: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    target_role: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_eduoffice_or_admin(current_user)

    # Get existing announcement
    existing = get_announcement_by_id(db, announcement_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Announcement not found")

    # Validate file type if provided
    if file and file.filename:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed"
            )

    # Save file if provided
    file_path = None
    file_name = None
    if file and file.filename:
        file_path = save_uploaded_file(file)
        file_name = file.filename

    # Prepare update data
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if message is not None:
        update_data["message"] = message
    if category is not None:
        update_data["category"] = category
    if target_role is not None:
        update_data["target_role"] = target_role
    if file_name is not None:
        update_data["file_name"] = file_name

    announcement_update = AnnouncementUpdate(**update_data)

    updated = update_announcement(db, announcement_id, announcement_update, file_path)
    if not updated:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return updated


@router.delete("/{announcement_id}")
async def delete_existing_announcement(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_eduoffice_or_admin(current_user)
    if not delete_announcement(db, announcement_id):
        raise HTTPException(status_code=404, detail="Announcement not found")
    return {"message": "Announcement deleted successfully"}


@router.get("/{announcement_id}/download")
async def download_announcement_file(
    announcement_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download the PDF file attached to an announcement."""
    announcement = get_announcement_by_id(db, announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    if not announcement.file_path:
        raise HTTPException(status_code=404, detail="No file attached to this announcement")

    # Check if user can access this announcement
    can_access = False
    if current_user.role == "admin" or current_user.role == "eduoffice":
        can_access = True
    elif current_user.role == "student" and announcement.target_role in ["student", "both"]:
        can_access = True
    elif current_user.role == "teacher" and announcement.target_role in ["teacher", "both"]:
        can_access = True

    if not can_access:
        raise HTTPException(status_code=403, detail="You don't have permission to access this file")

    file_path = Path("uploads") / announcement.file_path
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    from fastapi.responses import FileResponse
    return FileResponse(
        path=file_path,
        filename=announcement.file_name or f"announcement_{announcement_id}.pdf",
        media_type="application/pdf"
    )