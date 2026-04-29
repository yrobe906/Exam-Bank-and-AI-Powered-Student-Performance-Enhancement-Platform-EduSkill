from database import SessionLocal
from app.models.exam_attempt_models import ExamAttemptModel
from app.models.student_answer_models import StudentAnswerModel

db = SessionLocal()

# Check exam attempts for student 1
attempts = db.query(ExamAttemptModel).filter(ExamAttemptModel.student_id == 1).all()
print(f'Total exam attempts for student 1: {len(attempts)}')
print('\nFirst 5 attempts:')
for a in attempts[:5]:
    print(f'  Attempt ID: {a.id}, Exam ID: {a.exam_id}, Score: {a.score}')
    # Check student answers for this attempt
    answers = db.query(StudentAnswerModel).filter(StudentAnswerModel.attempt_id == a.id).all()
    print(f'    Answers count: {len(answers)}')
    correct_count = sum(1 for ans in answers if ans.is_correct)
    print(f'    Correct answers: {correct_count}')
    if answers:
        print(f'    Score percentage: {(correct_count/len(answers))*100:.2f}%')

db.close()
