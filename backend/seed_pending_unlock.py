import sys
sys.path.append('.')

from database import SessionLocal, engine
from app.models import *
from app.models.user_models import User
from app.models.exam_models import ExamModel
from app.models.unlock_models_fixed import StudentExamUnlockRequest
from app.crud.unlock_crud_fixed import service_create_unlock_request
from app.schemas.unlock_schemas import UnlockRequestCreate
from passlib.context import PasswordContext
from sqlalchemy.exc import IntegrityError

db = SessionLocal()

# Helper
def hash_password(password):
    pwd_context = PasswordContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

# 1. Create test student
try:
    student = db.query(User).filter(User.email == "student@test.com").first()
    if not student:
        student = User(
            full_name="Test Student",
            email="student@test.com",
            role="student",
            hashed_password=hash_password("student123")
        )
        db.add(student)
        db.commit()
        print(f"✅ Created student ID: {student.id}")
    else:
        print(f"✅ Student exists ID: {student.id}")
except Exception as e:
    print(f"❌ Student error: {e}")
    db.rollback()

# 2. Add XP points to student (for points method test)
try:
    from app.models.gamification_models import UserGamificationStats
    stats = db.query(UserGamificationStats).filter(UserGamificationStats.user_id == student.id).first()
    if not stats:
        stats = UserGamificationStats(
            user_id=student.id,
            xp_points=1000,
            total_xp_earned=1000,
            tier="silver"
        )
        db.add(stats)
        db.commit()
        print("✅ Created gamification stats")
    else:
        stats.xp_points = 1000
        db.commit()
        print("✅ Updated XP to 1000")
except Exception as e:
    print(f"❌ Gamification error: {e}")
    db.rollback()

# 3. Create test exam
try:
    exam = db.query(ExamModel).filter(ExamModel.title == "Test Premium Exam").first()
    if not exam:
        exam = ExamModel(
            name="Test Premium Exam",
            title="Test Premium Exam",
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
except Exception as e:
    print(f"❌ Exam error: {e}")
    db.rollback()

# 4. Create pending unlock request (points method)
try:
    request = db.query(StudentExamUnlockRequest).filter(
        StudentExamUnlockRequest.student_id == student.id,
        StudentExamUnlockRequest.exam_id == exam.id,
        StudentExamUnlockRequest.status == "pending"
    ).first()
    if not request:
        req_data = UnlockRequestCreate(
            exam_id=exam.id,
            unlock_method="points"
        )
        # Use service (admin bypass for seed)
from app.services.unlock_service_fixed import service_create_unlock_request
        processed = service_create_unlock_request(
            db, student.id, req_data.exam_id, req_data.unlock_method, 
            None, None  # no payment
        )
        print(f"✅ Created pending request ID: {processed.id}")
    else:
        print("✅ Pending request exists")
except Exception as e:
    print(f"❌ Request error: {e}")
    db.rollback()

# 5. Create test admin
try:
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            full_name="Test Admin",
            email="admin@example.com",
            role="admin",
            hashed_password=hash_password("admin123")
        )
        db.add(admin)
        db.commit()
        print(f"✅ Created admin ID: {admin.id}")
    else:
        print("✅ Admin exists")
except Exception as e:
    print(f"❌ Admin error: {e}")
    db.rollback()

db.close()
print("🎉 Seeding complete! Test data ready.")

