"""Seed XP to test gamification - awards XP to first 5 students via direct DB ops (avoids model import issues)."""
from sqlalchemy.orm import Session
from sqlalchemy import update
from database import SessionLocal
from app.models.user_models import User
from app.models.gamification_models import GamificationActivityModel
from app.utils.gamification_utils import get_tier
from datetime import datetime, timedelta

def seed_xp():
    db = SessionLocal()
    try:
        # Get ALL students
        students = db.query(User).filter(User.role == 'student').all()
        
        for student in students:
            print(f"Seeding XP for {student.username} (ID: {student.id})")
            
            # Direct XP update (simulate awards)
            total_xp = 55  # Matches activities: 20 sub + 15 result + 10 login + 10 prev login
            student.xp_points += total_xp
            student.current_tier = get_tier(student.xp_points)
            
            # Add sample activities
            activities = [
                GamificationActivityModel(
                    user_id=student.id,
                    activity_type='exam_submission',
                    content_id=1,
                    xp_awarded=20,
                    created_at=datetime.now() - timedelta(hours=2)
                ),
                GamificationActivityModel(
                    user_id=student.id,
                    activity_type='exam_result',
                    content_id=1,
                    xp_awarded=15,
                    created_at=datetime.now() - timedelta(hours=1)
                ),
                GamificationActivityModel(
                    user_id=student.id,
                    activity_type='daily_login',
                    xp_awarded=10,
                    created_at=datetime.now()
                ),
                GamificationActivityModel(
                    user_id=student.id,
                    activity_type='daily_login',
                    xp_awarded=10,
                    created_at=datetime.now() - timedelta(days=1)
                )
            ]
            db.add_all(activities)
            print(f"  Added {total_xp} XP, 4 activities. Final: {student.xp_points} XP, Tier: {student.current_tier}")
        
        db.commit()
        print("Seeding complete! Check /gamification/profile or Gamification.vue")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_xp()

