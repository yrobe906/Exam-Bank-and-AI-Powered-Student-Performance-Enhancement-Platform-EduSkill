from database import SessionLocal
from app.models import *
from app.models.user_models import User
from app.models.exam_models import ExamModel
from app.models.unlock_models_fixed import UnlockRequestModel
# XP stored directly on User model, no separate stats table
from passlib.context import PasswordContext
from sqlalchemy.exc import IntegrityError

db = SessionLocal()

pwd_context = PasswordContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

# Clear previous test data (optional)
print("🧹 Clearing previous test data...")
db.query(UnlockRequestModel).filter(
    UnlockRequestModel.user_id.in_([1,2]),
    UnlockRequestModel.exam_id.in_([1,2])
).delete()
db.query(UserGamificationStats).filter(
    UserGamificationStats.user_id.in_([1,2])
).delete()
db.commit()

# 1. Create test student ID=1
student_email = "student@test.com"
student = db.query(User).filter(User.email == student_email).first()
if not student:
    student = User(
        full_name="Test Student",
        email=student_email,
        role="student",
        hashed_password=hash_password("student123")
    )
    db.add(student)
    db.commit()
    print(f"✅ Created student ID: {student.id}")
else:
    print(f"✅ Student exists ID: {student.id}")

# 2. Add XP=1000 to student
student.xp_points = 1000
student.current_tier = "silver"
db.commit()
print("✅ Set student XP=1000")

# 3. Create test exam ID=1
exam_title = "Test Premium Exam"
exam = db.query(ExamModel).filter(ExamModel.title == exam_title).first()
if not exam:
    exam = ExamModel(
        name=exam_title,
        title=exam_title,
        description="Premium exam for unlock testing",
        amount=100.0,
        duration=60,
        total_questions=50,
        pricing_type="Premium"
    )
    db.add(exam)
    db.commit()
    print(f"✅ Created exam ID: {exam.id}")
else:
    print(f"✅ Exam exists ID: {exam.id}")

# 4. Create pending unlock request (points)
existing_request = db.query(UnlockRequestModel).filter(
    UnlockRequestModel.user_id == student.id,
    UnlockRequestModel.exam_id == exam.id,
    UnlockRequestModel.status == "pending"
).first()
if not existing_request:
    from app.crud.unlock_crud_fixed import create_unlock_request
    from app.models.exam_models import ExamModel as ExamType  # type hint
    request = create_unlock_request(
        db, 
        student.id, 
        exam.id, 
        "points",
        points_required=200,  # for 100 ETB
        price=exam.amount
    )
    db.commit()
    print(f"✅ Created pending request ID: {request.id}")
else:
    print("✅ Pending request exists")

# 5. Create test admin ID=2
admin_email = "admin@example.com"
admin = db.query(User).filter(User.email == admin_email).first()
if not admin:
    admin = User(
        full_name="Test Admin",
        email=admin_email,
        role="admin",
        hashed_password=hash_password("admin123")
    )
    db.add(admin)
    db.commit()
    print(f"✅ Created admin ID: {admin.id}")
else:
    print("✅ Admin exists")

db.close()
print("\n🎉 Seeding complete!")
print("🌐 Backend: http://localhost:8000/docs")
print("🔑 Student: student@test.com / student123")
print("🔑 Admin: admin@example.com / admin123")
print("🧪 Test Premium: /premium?examId=1")
print("📊 Admin unlocks: /admin/unlock-requests")

