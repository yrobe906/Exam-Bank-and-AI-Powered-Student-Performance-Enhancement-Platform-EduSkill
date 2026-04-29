from database import SessionLocal, engine
from app.models import *

db = SessionLocal()

print("Creating test users, exam, pending unlock...")

# Create test student
student = db.query(User).filter(User.email == 'teststudent@issms.com').first()
if not student:
    student = User(
        full_name='Test Student',
        username='teststudent',
        email='teststudent@issms.com',
        password_hash='$2b$12$K.1v3hMN4g6Z9v4W2q9K.uI8jX3n7p1X6Z1p5T2r8v9W0x3Y4Z5A',  # dummy hash 'test123'
        role='student',
        gender='M',
        grade=10,
        xp_points=1000,
        current_tier='silver',
        status='approved'
    )
    db.add(student)
    db.commit()
    print(f'✅ Student created ID: {student.id}')
else:
    print(f'✅ Student exists ID: {student.id}')
    student.xp_points = 1000
    student.current_tier = 'silver'
    db.commit()

# Create test admin
admin = db.query(User).filter(User.email == 'testadmin@issms.com').first()
if not admin:
    admin = User(
        full_name='Test Admin',
        username='testadmin',
        email='testadmin@issms.com',
        password_hash='$2b$12$K.1v3hMN4g6Z9v4W2q9K.uI8jX3n7p1X6Z1p5T2r8v9W0x3Y4Z5A',
        role='admin',
        gender='M',
        status='approved'
    )
    db.add(admin)
    db.commit()
    print(f'✅ Admin created ID: {admin.id}')
else:
    print(f'✅ Admin exists ID: {admin.id}')

# Create test premium exam
exam = db.query(ExamModel).filter(ExamModel.name == 'Test Premium Unlock Exam').first()
if not exam:
    exam = ExamModel(
        sector_id=1,
        name='Test Premium Unlock Exam',
        total_questions=50,
        duration=60,
        total_marks=100,
        exam_type='mock_exam',
        pricing_type='Premium',
        amount=100.0,
        description='For button click testing'
    )
    db.add(exam)
    db.commit()
    print(f'✅ Exam created ID: {exam.id}')
else:
    print(f'✅ Exam exists ID: {exam.id}')

# Create pending unlock request
existing = db.query(UnlockRequestModel).filter(
    UnlockRequestModel.user_id == student.id,
    UnlockRequestModel.exam_id == exam.id,
    UnlockRequestModel.status == 'pending'
).first()
if not existing:
    request = UnlockRequestModel(
        user_id=student.id,
        exam_id=exam.id,
        content_type='mock_exam',
        exam_name=exam.name,
        unlock_method='points',
        points_required=200,
        price=100.0,
        status='pending'
    )
    db.add(request)
    db.commit()
    print(f'✅ Pending request created ID: {request.id}')
else:
    print('✅ Pending request exists')

db.close()
print('\n🎉 Ready!')
print('Login: teststudent@issms.com / test123 (student)')
print('Login: testadmin@issms.com / test123 (admin)')
print('Premium: /premium?examId=X (use exam ID above)')
print('Admin unlocks: /api/admin/unlock/requests')
