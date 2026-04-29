from pydantic import BaseModel
from typing import Optional

class ExamStructureCreate(BaseModel):
    exam_type: str
    year: Optional[int] = None
    university: Optional[str] = None
    model_type: Optional[str] = None
    subject: str
    topic: str
