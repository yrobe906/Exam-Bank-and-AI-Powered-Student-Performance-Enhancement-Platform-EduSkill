"""
Seed script to add default gamification data (thresholds, badges)
Run this after creating tables to populate initial data
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine, Base

# Import only gamification models to avoid relationship issues
from app.models.gamification_models import ContentXPThreshold, Badge

# Create tables if not exist
Base.metadata.create_all(bind=engine)


def seed_data():
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_thresholds = db.query(ContentXPThreshold).count()
        if existing_thresholds > 0:
            print("Content thresholds already exist. Skipping...")
        else:
            # Add default content XP thresholds
            thresholds = [
                # Study Notes
                ContentXPThreshold(content_type="study_note", tier_required="silver", xp_required=100),
                ContentXPThreshold(content_type="study_note", tier_required="gold", xp_required=200),
                ContentXPThreshold(content_type="study_note", tier_required="diamond", xp_required=300),
                
                # Videos
                ContentXPThreshold(content_type="video", tier_required="silver", xp_required=100),
                ContentXPThreshold(content_type="video", tier_required="gold", xp_required=200),
                ContentXPThreshold(content_type="video", tier_required="diamond", xp_required=300),
                
                # Mock Tests
                ContentXPThreshold(content_type="mock_test", tier_required="gold", xp_required=150),
                ContentXPThreshold(content_type="mock_test", tier_required="diamond", xp_required=250),
                
                # Mock Exams
                ContentXPThreshold(content_type="mock_exam", tier_required="gold", xp_required=200),
                ContentXPThreshold(content_type="mock_exam", tier_required="diamond", xp_required=350),
            ]
            
            for threshold in thresholds:
                db.add(threshold)
            
            db.commit()
            print("Added default content XP thresholds")
        
        # Check if badges already exist
        existing_badges = db.query(Badge).count()
        if existing_badges > 0:
            print("Badges already exist. Skipping...")
        else:
            # Add default badges
            badges = [
                Badge(
                    name="First Steps",
                    description="Complete your first exam",
                    tier_required="bronze",
                    xp_required=0,
                    streak_required=0,
                    content_type="exam"
                ),
                Badge(
                    name="Quick Learner",
                    description="Score 60% or above on an exam",
                    tier_required="bronze",
                    xp_required=20,
                    streak_required=0,
                    content_type="exam"
                ),
                Badge(
                    name="Study Starter",
                    description="Achieve a 3-day study streak",
                    tier_required="bronze",
                    xp_required=0,
                    streak_required=3,
                    content_type=None
                ),
                Badge(
                    name="Silver Scholar",
                    description="Reach Silver tier",
                    tier_required="silver",
                    xp_required=300,
                    streak_required=0,
                    content_type=None
                ),
                Badge(
                    name="Consistent Learner",
                    description="Achieve a 7-day study streak",
                    tier_required="silver",
                    xp_required=50,
                    streak_required=7,
                    content_type=None
                ),
                Badge(
                    name="Gold Graduate",
                    description="Reach Gold tier",
                    tier_required="gold",
                    xp_required=600,
                    streak_required=0,
                    content_type=None
                ),
                Badge(
                    name="High Achiever",
                    description="Score 90% or above on an exam",
                    tier_required="gold",
                    xp_required=100,
                    streak_required=0,
                    content_type="exam"
                ),
                Badge(
                    name="Diamond Master",
                    description="Reach Diamond tier",
                    tier_required="diamond",
                    xp_required=3000,
                    streak_required=10,
                    content_type=None
                ),
                Badge(
                    name="Study Champion",
                    description="Achieve a 30-day study streak",
                    tier_required="diamond",
                    xp_required=500,
                    streak_required=30,
                    content_type=None
                ),
                Badge(
                    name="Premium Unlocked",
                    description="Unlock your first premium content",
                    tier_required="silver",
                    xp_required=50,
                    streak_required=0,
                    content_type="premium"
                ),
            ]
            
            for badge in badges:
                db.add(badge)
            
            db.commit()
            print("Added default badges")
        
        print("\nGamification data seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
