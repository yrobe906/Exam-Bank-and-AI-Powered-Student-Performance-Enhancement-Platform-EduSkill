from database import SessionLocal
from app.models.exam_attempt_models import ExamAttemptModel
from app.models.student_answer_models import StudentAnswerModel
from app.models.user_models import User

db = SessionLocal()

# Check if student 6 exists
student = db.query(User).filter(User.id == 6).first()
print(f'Student 6 exists: {student}')
if student:
    print(f'  Student name: {student.username}, Role: {student.role}')

# Check all exam attempts
all_attempts = db.query(ExamAttemptModel).all()
print(f'\nTotal exam attempts in system: {len(all_attempts)}')

# Group by student
from sqlalchemy import func
student_counts = db.query(
    ExamAttemptModel.student_id, 
    func.count(ExamAttemptModel.id)
).group_by(ExamAttemptModel.student_id).all()
print('\nExam attempts per student:')
for student_id, count in student_counts:
    print(f'  Student {student_id}: {count} attempts')

# Check exam attempts for student 6
attempts = db.query(ExamAttemptModel).filter(ExamAttemptModel.student_id == 6).all()
print(f'\nTotal exam attempts for student 6: {len(attempts)}')
for a in attempts:
    print(f'  Attempt ID: {a.id}, Exam ID: {a.exam_id}, Score: {a.score}')
    # Check student answers for this attempt
    answers = db.query(StudentAnswerModel).filter(StudentAnswerModel.attempt_id == a.id).all()
    print(f'    Answers count: {len(answers)}')
    for ans in answers[:3]:  # Show first 3 answers
        print(f'      Question ID: {ans.question_id}, Correct: {ans.is_correct}')

db.close()
