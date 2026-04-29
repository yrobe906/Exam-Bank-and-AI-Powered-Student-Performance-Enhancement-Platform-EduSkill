from database import SessionLocal, engine
from app.models.downloadable_models_fixed import ModelExam, EntranceExam
from database import Base
from sqlalchemy import event
from pathlib import Path

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

def seed_data():
    # Clear existing (soft delete)
    db.query(ModelExam).filter(ModelExam.is_active == True).update({ModelExam.is_active: False})
    db.query(EntranceExam).filter(EntranceExam.is_active == True).update({EntranceExam.is_active: False})
    db.commit()
    
    # Sample Model Exams
    model_exams = [
        ModelExam(
            title='Grade 12 Mathematics Model Exam 1',
            stream='natural',
            subject='Mathematics',
            institution='Addis Ababa University',
            institution_type='University',
            creator='Prof. Abebe Kebede',
            file_path='uploads/downloadables/mock_math.pdf',
            file_name='mock_math.pdf',
            file_size='2.4 MB',
            file_type='PDF',
            uploaded_by=1  # sample user
        ),
        ModelExam(
            title='Physics Practice Test Vol 1',
            stream='natural',
            subject='Physics',
            institution='Bahir Dar University',
            institution_type='University',
            creator='Dr. Selam Aweke',
            file_path='uploads/downloadables/mock_physics.pdf',
            file_name='mock_physics.pdf',
            file_size='1.8 MB',
            file_type='PDF',
            uploaded_by=1
        ),
        ModelExam(
            title='Economics Midterm Model',
            stream='social',
            subject='Economics',
            institution='Jimma University',
            institution_type='University',
            creator='Prof. Fatima Ali',
            file_path='uploads/downloadables/mock_econ.pdf',
            file_name='mock_econ.pdf',
            file_size='1.9 MB',
            file_type='PDF',
            uploaded_by=1
        )
    ]
    
    # Sample Entrance Exams
    entrance_exams = [
        EntranceExam(
            title='National Entrance Math 2023',
            year=2023,
            stream='natural',
            subject='Mathematics',
            institution='Ministry of Education',
            creator='Exam Board',
            file_path='uploads/downloadables/entrance_math_2023.pdf',
            file_name='entrance_math_2023.pdf',
            file_size='4.5 MB',
            file_type='PDF',
            uploaded_by=1
        ),
        EntranceExam(
            title='Social Science Entrance 2024',
            year=2024,
            stream='social',
            subject='Economics',
            institution='Ministry of Education',
            creator='Exam Board',
            file_path='uploads/downloadables/entrance_social_2024.pdf',
            file_name='entrance_social_2024.pdf',
            file_size='4.8 MB',
            file_type='PDF',
            uploaded_by=1
        )
    ]
    
    for exam in model_exams + entrance_exams:
        db.add(exam)
    
    db.commit()
    print('✅ Seeded', len(model_exams), 'ModelExams +', len(entrance_exams), 'EntranceExams')

seed_data()
db.close()
print('Database seeded successfully!')

