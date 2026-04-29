# app/schemas/exam_schemas.py
from pydantic import BaseModel
from typing import Optional, List

# -------------------
# Sector schemas
# -------------------
class SectorBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None

class SectorOut(SectorBase):
    id: int

    class Config:
        from_attributes = True  # For Pydantic v2

# -------------------
# Exam schemas
# -------------------
class ExamBase(BaseModel):
    name: str
    sector_id: int
    total_questions: int
    duration: int  # in minutes
    total_marks: int
    exam_type: str
    pricing_type: Optional[str] = "Free"  # "Free" or "Premium"
    amount: Optional[float] = 0  # Amount in ETB for premium exams

class ExamOut(ExamBase):
    id: int

    class Config:
        from_attributes = True

# This is the schema you were missing
class ExamDetailOut(BaseModel):
    id: int
    name: str
    sector_id: int
    total_questions: int
    duration: int
    total_marks: int
    exam_type: str
    pricing_type: Optional[str] = "Free"
    amount: Optional[float] = 0
    sections: List["SectionOut"] = []

    class Config:
        from_attributes = True

# -------------------
# Section schemas
# -------------------
class SectionBase(BaseModel):
    name: str
    exam_id: int
    question_count: int
    color: Optional[str] = None

class SectionOut(SectionBase):
    id: int
    questions: List["QuestionOut"] = []

    class Config:
        from_attributes = True

# -------------------
# Question schemas
# -------------------
class QuestionBase(BaseModel):
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    difficulty: int
    marks: int
    section_id: int

class QuestionOut(QuestionBase):
    id: int

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    section_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    difficulty: int
    marks: int

# -------------------
# Test schemas
# -------------------
class TestCreate(BaseModel):
    title: str
    sector_id: Optional[int] = None
    exam_id: Optional[int] = None
    duration: int
    difficulty: int
    question_count: int
    created_by: Optional[int] = None

# -------------------
# Fix forward references
# -------------------
SectionOut.update_forward_refs()
ExamDetailOut.update_forward_refs()
