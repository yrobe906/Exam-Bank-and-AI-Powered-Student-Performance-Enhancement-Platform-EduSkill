from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResourceBase(BaseModel):
    title: str
    description: str
    type: str
    subject: str
    grade_level: str
    is_premium: bool = False
    price: float = 0

class ResourceCreate(ResourceBase):
    pass

class ResourceResponse(ResourceBase):
    id: int
    file_name: str
    file_path: str  # ADDED this field
    file_size: int
    uploaded_by: int
    created_at: datetime
    is_active: bool
    preview_path: Optional[str] = None  # ADDED this field
    
    class Config:
        from_attributes = True

# Optional: Add a schema for student view (hides file_path for security)
class ResourceStudentView(ResourceResponse):
    can_access: bool = False