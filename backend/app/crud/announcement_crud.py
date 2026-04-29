from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.announcement_models import Announcement
from ..schemas.announcement_schemas import AnnouncementCreate, AnnouncementUpdate
import os
from pathlib import Path


def get_announcements(db: Session, role: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Announcement]:
    query = db.query(Announcement).filter(Announcement.is_active == True)
    if role:
        if role == "student":
            query = query.filter(Announcement.target_role.in_(["student", "both"]))
        elif role == "teacher":
            query = query.filter(Announcement.target_role.in_(["teacher", "both"]))
    return query.offset(skip).limit(limit).all()


def get_announcement_by_id(db: Session, announcement_id: int) -> Optional[Announcement]:
    return db.query(Announcement).filter(Announcement.id == announcement_id).first()


def create_announcement(db: Session, announcement: AnnouncementCreate, file_path: Optional[str] = None) -> Announcement:
    db_announcement = Announcement(**announcement.dict())
    if file_path:
        db_announcement.file_path = file_path
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement


def update_announcement(db: Session, announcement_id: int, announcement_update: AnnouncementUpdate, file_path: Optional[str] = None) -> Optional[Announcement]:
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        return None

    update_data = announcement_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_announcement, field, value)

    if file_path:
        # Delete old file if exists
        if db_announcement.file_path:
            try:
                old_file_path = Path("uploads") / db_announcement.file_path
                if old_file_path.exists():
                    old_file_path.unlink()
            except Exception as e:
                print(f"Error deleting old file: {e}")

        db_announcement.file_path = file_path

    db.commit()
    db.refresh(db_announcement)
    return db_announcement


def delete_announcement(db: Session, announcement_id: int) -> bool:
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        return False

    # Delete associated file if exists
    if db_announcement.file_path:
        try:
            file_path = Path("uploads") / db_announcement.file_path
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            print(f"Error deleting file: {e}")

    db.delete(db_announcement)
    db.commit()
    return True