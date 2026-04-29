from database import SessionLocal
from app.models.section_feedback_models import SectionFeedback
from app.models.user_models import User
from app.models.section_models import SectionModel
from datetime import datetime

db = SessionLocal()

# Get some users and sections
users = db.query(User).filter(User.role == 'student').limit(5).all()
sections = db.query(SectionModel).limit(5).all()

if users and sections:
    for i in range(10):
        user = users[i % len(users)]
        section = sections[i % len(sections)]
        feedback = SectionFeedback(
            section_id=section.id,
            user_id=user.id,
            feedback_text=f"Test feedback {i+1} for section {section.name}",
            is_anonymous=False,
            rating=(i % 5) + 1,
            status='pending'
        )
        db.add(feedback)
    
    db.commit()
    print("Test feedback added")
else:
    print("No users or sections found")

db.close()