"""
Migration script to add gamification tables to the database
Run this script to create all new gamification-related tables
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base
from app.models.gamification_models import (
    StudentProfile,
    Badge,
    XPTransaction,
    UnlockRequest,
    ContentUnlock,
    ActivityLog,
    XPCooldown,
    ContentXPThreshold
)


def run_migration():
    print("Creating gamification tables...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("StudentProfile table created")
    print("Badge table created")
    print("XPTransaction table created")
    print("UnlockRequest table created")
    print("ContentUnlock table created")
    print("ActivityLog table created")
    print("XPCooldown table created")
    print("ContentXPThreshold table created")
    
    print("\nAll gamification tables created successfully!")


if __name__ == "__main__":
    run_migration()
