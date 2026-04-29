from sqlalchemy.orm import Session
from app.models.resource_models import Resource
from sqlalchemy import or_
from typing import Optional, List

def create_resource(
    db: Session, 
    resource_data: dict, 
    file_name: str, 
    file_path: str,
    file_size: int,
    uploaded_by: int
) -> Resource:
    try:
        db_resource = Resource(
            **resource_data,
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            uploaded_by=uploaded_by
        )
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
        return db_resource
    except Exception as e:
        db.rollback()
        raise e

def get_resources(
    db: Session, 
    grade: Optional[str] = None, 
    type: Optional[str] = None, 
    subject: Optional[str] = None,
    search: Optional[str] = None,
    is_premium: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Resource]:
    query = db.query(Resource).filter(Resource.is_active == True)
    
    if grade:
        query = query.filter(Resource.grade_level == grade)
    if type:
        query = query.filter(Resource.type == type)
    if subject:
        query = query.filter(Resource.subject.ilike(f"%{subject}%"))
    if is_premium is not None:
        query = query.filter(Resource.is_premium == is_premium)
    if search:
        query = query.filter(
            or_(
                Resource.title.ilike(f"%{search}%"),
                Resource.description.ilike(f"%{search}%"),
                Resource.subject.ilike(f"%{search}%")
            )
        )
    
    return query.offset(skip).limit(limit).order_by(Resource.created_at.desc()).all()

def get_resource(db: Session, resource_id: int) -> Optional[Resource]:
    return db.query(Resource).filter(
        Resource.id == resource_id, 
        Resource.is_active == True
    ).first()

def update_resource(db: Session, resource_id: int, update_data: dict) -> Optional[Resource]:
    resource = get_resource(db, resource_id)
    if resource:
        try:
            for key, value in update_data.items():
                setattr(resource, key, value)
            db.commit()
            db.refresh(resource)
        except Exception as e:
            db.rollback()
            raise e
    return resource

def delete_resource(db: Session, resource_id: int) -> bool:
    resource = get_resource(db, resource_id)
    if resource:
        try:
            resource.is_active = False
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
    return False