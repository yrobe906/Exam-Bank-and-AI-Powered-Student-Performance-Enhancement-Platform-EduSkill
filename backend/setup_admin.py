# setup_admin.py - Run this once to create admin user
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from app.models.admin import Admin
from passlib.context import CryptContext

# Fix for bcrypt error
import bcrypt as bcrypt_module

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(Admin).filter(Admin.email == "admin@example.com").first()
        if existing_admin:
            print("⚠️ Admin already exists")
            return
        
        # Create admin with all required fields
        admin = Admin(
            email="admin@example.com",
            username="admin",  # Added username
            full_name="System Administrator",
            hashed_password=pwd_context.hash("admin123"),
            role="admin",
            is_active=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("✅ Admin created successfully!")
        print(f"   ID: {admin.id}")
        print("   Email: admin@example.com")
        print("   Username: admin")
        print("   Password: admin123")
        
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        db.rollback()
        raise e  # Re-raise to see full error
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()