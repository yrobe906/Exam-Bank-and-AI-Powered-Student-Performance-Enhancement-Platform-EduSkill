from database import SessionLocal
from app.models.user_models import User
from app.utils.hashing import hash_password
from app.models import *

db = SessionLocal()

username = 'esma'
email = 'esma@example.com'
password = 'esma123'
password_hash = hash_password(password)

# Check if exists
existing = db.query(User).filter((User.username == username) | (User.email == email)).first()
if existing:
    print(f"User {username} already exists with status '{existing.status}'")
    # Update status to approved if not
    if existing.status != 'approved':
        existing.status = 'approved'
        db.commit()
        print("Status updated to approved")
else:
    user = User(
        full_name='Esma Test Student',
        username=username,
        email=email,
        password_hash=password_hash,
        role='student',
        gender='F',
        grade=10,
        status='approved',
        xp_points=0,
        current_tier='bronze'
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✅ Created esma user ID: {user.id}")

print(f"Login test: username='{username}' or email='{email}', password='{password}'")
print("Status: approved")
print("Expected log: User found: esma, status: approved")
print("\\nRun POST /api/users/login to test.")

db.close()
print('🎉 Seed complete!')

