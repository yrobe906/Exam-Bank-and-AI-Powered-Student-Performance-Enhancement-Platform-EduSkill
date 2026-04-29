from database import SessionLocal
from app.models import *
db = SessionLocal()

print("Final simple seed for button test...")

# Use sector 1, create exam, student, pending request

# Student
student = User(
    full_name='Test Student',
    username='teststud',
    email='teststud@issms.com',
    password_hash='$2b$12$EoH0Pi6f7g8Y9z1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S', 
    role='student',
    gender='M',
    grade=10,
    xp_points=1000,
    current_tier='silver',
    status='approved'
)
db.add(student)
db.flush()
print(f'Student ID: {student.id}')

# Exam with sector_id=1
exam = ExamModel(
    sector_id=1,
    name='Test Premium Exam for Buttons',
    total_questions=50,
    duration=60,
    total_marks=100,
    exam_type='mock_exam',
    pricing_type='Premium',
    amount=100.0
)
db.add(exam)
db.flush()
print(f'Exam ID: {exam.id}')

# Pending request
        request = UnlockRequestModel(
        user_id=student.id,
        exam_id=exam.id,
        content_id=exam.id,
        content_type='mock_exam',
        exam_name=exam.name,
        unlock_method='points',
        points_required=200,
        price=100.0,
        status='pending'
    )
db.add(request)
db.commit()
print(f'Pending request ID: {request.id}')

# Admin
admin = User(
    full_name='Test Admin',
    username='testadmin',
    email='testadmin@issms.com',
    password_hash='$2b$12$EoH0Pi6f7g8Y9z1A2b3C4d5E6f7G8h9I0j1K2l3M4n5O6p7Q8r9S',
    role='admin',
    gender='M',
    status='approved'
)
db.add(admin)
db.commit()
print('Admin created')

db.close()
print('\\n✅ Test data ready!')
print('Passwords: test123 for both')
print('Use /premium?examId=[exam ID above]')
print('Admin page will show pending request')
