from sqlalchemy.orm import Session
from app.models import sector_models, exam_models, section_models, question_models, test_models
from app.schemas import exam_schemas

class ExamService:
    
    @staticmethod
    def get_sectors(db: Session):
        """Get all sectors"""
        return db.query(sector_models.Sector).all()
    
    @staticmethod
    def get_exams_by_sector(db: Session, sector_id: int):
        """Get exams filtered by sector"""
        return db.query(exam_models.Exam).filter(exam_models.Exam.sector_id == sector_id).all()
    
    @staticmethod
    def get_sections_by_exam(db: Session, exam_id: int):
        """Get sections filtered by exam"""
        return db.query(section_models.Section).filter(section_models.Section.exam_id == exam_id).all()
    
    @staticmethod
    def get_questions_by_sections(db: Session, section_ids: List[int], difficulty: Optional[int] = None):
        """Get questions from multiple sections"""
        query = db.query(question_models.Question).filter(
            question_models.Question.section_id.in_(section_ids)
        )
        if difficulty is not None:
            query = query.filter(question_models.Question.difficulty == difficulty)
        return query.all()
    
    @staticmethod
    def create_test(db: Session, test_data: exam_schemas.TestCreate, is_draft: bool = True):
        """Create a new test"""
        new_test = test_models.Test(
            title=test_data.title,
            sector_id=test_data.sector_id,
            exam_id=test_data.exam_id,
            duration=test_data.duration,
            difficulty=test_data.difficulty,
            question_count=test_data.question_count,
            created_by=test_data.created_by or 1,
            is_draft=is_draft
        )
        db.add(new_test)
        db.commit()
        db.refresh(new_test)
        return new_test