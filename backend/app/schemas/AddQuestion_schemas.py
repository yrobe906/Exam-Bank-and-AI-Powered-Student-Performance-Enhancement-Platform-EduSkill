from pydantic import BaseModel
from typing import Optional

class QuestionCreate(BaseModel):
    structure_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    difficulty: str
    explanation: Optional[str] = None
    pdf_file: Optional[str] = None  # optional PDF filename

class QuestionUpdate(BaseModel):
    structure_id: Optional[int]
    question_text: Optional[str]
    option_a: Optional[str]
    option_b: Optional[str]
    option_c: Optional[str]
    option_d: Optional[str]
    correct_answer: Optional[str]
    difficulty: Optional[str]
    explanation: Optional[str]
    pdf_file: Optional[str]
