from database import SessionLocal
from app.models import *

db = SessionLocal()

print("🧹 Clearing old test data...")
db.query(UnlockRequestModel).filter(
    UnlockRequestModel.exam_name.ilike('%test%premium%')
).delete()
db.commit()

# Create simple pending request directly
user = db.query(User).filter(User.email == "student@test.com").first()
if not user:
    print("❌ No student@test.com - create via UI first")
else:
    exam = db.query(ExamModel).filter(ExamModel.title.ilike('%test%premium%')).first()
    if not exam:
        print("❌ No test premium exam - create via UI")
    else:
        # Direct create pending request
        request = UnlockRequestModel(
            user_id=user.id,
            exam_id=exam.id,
            content_type="mock_exam",
            exam_name=exam.title,
            unlock_method="points",
            points_required=200,
            price=100.0,
            status="pending"
        )
        db.add(request)
        db.commit()
        print(f"✅ Created pending unlock request ID: {request.id} for student {user.id}, exam {exam.id}")

# XP on user
user.xp_points = 1000 if hasattr(user, 'xp_points') else None
if hasattr(user, 'current_tier'):
    user.current_tier = "silver"
db.commit()
print(f"✅ Student {user.id} XP set")

print("\n🎉 Simple seeding complete!")
print("Login as student@test.com/student123 or admin@example.com/admin123")
print("Go to Premium page ?examId=1 and Admin unlocks page")
