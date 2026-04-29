# Exam CRUD functions
from app.models.exam_models import ExamModel
from sqlalchemy.orm import Session

def create_exam(db: Session, exam_data):
	exam = ExamModel(
		name=exam_data.name,
		sector_id=exam_data.sector_id,
		total_questions=exam_data.total_questions,
		duration=exam_data.duration,
		total_marks=exam_data.total_marks,
		exam_type=exam_data.exam_type
	)
	db.add(exam)
	db.commit()
	db.refresh(exam)
	return exam

def get_exam(db: Session, exam_id: int):
	return db.query(ExamModel).filter(ExamModel.id == exam_id).first()

def get_exams(db: Session, sector_id=None):
	query = db.query(ExamModel)
	if sector_id:
		query = query.filter(ExamModel.sector_id == sector_id)
	return query.all()

def update_exam(db: Session, exam_id: int, exam_data):
	exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
	if not exam:
		return None
	exam.name = exam_data.name
	exam.sector_id = exam_data.sector_id
	exam.total_questions = exam_data.total_questions
	exam.duration = exam_data.duration
	exam.total_marks = exam_data.total_marks
	exam.exam_type = exam_data.exam_type
	db.commit()
	db.refresh(exam)
	return exam
