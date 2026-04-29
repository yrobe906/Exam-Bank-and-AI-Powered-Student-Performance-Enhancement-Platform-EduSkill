from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    title: str
    subject: str
    category: str
    content: str
    access_type: str = "free"
    price: float = 0.0
    theme_color: str = "blue"
    font_style: str = "sans-serif"

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    access_type: Optional[str] = None
    price: Optional[float] = None
    theme_color: Optional[str] = None
    font_style: Optional[str] = None
    uploaded_by: Optional[int] = None

class NoteResponse(NoteBase):
    id: int
    uploaded_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LibraryCountsResponse(BaseModel):
    """Response schema for library counts aggregation"""
    notes_count: int
    slides_count: int
    videos_count: int
    books_count: int
    total_resources: int
    free_resources: int
    premium_resources: int
    total_notes: int
    free_notes: int
    premium_notes: int
