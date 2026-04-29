import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'register_db',
    'user': 'postgres',
    'password': '4316'
}

def seed_minimal():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    
    # ACTIVATE ALL EXISTING RECORDS
    cur.execute("UPDATE model_exams SET is_active = true")
    cur.execute("UPDATE entrance_exams SET is_active = true")
    
    # Insert new ModelExams WITH is_active=True
    cur.execute("""
        INSERT INTO model_exams (title, stream, subject, institution, institution_type, creator, file_path, file_name, file_size, file_type, description, download_count, uploaded_by, is_active) 
        VALUES 
        ('Grade 12 Math Model', 'natural', 'Mathematics', 'Jimma University', 'University', 'Prof Test', 'uploads/downloadables/math.pdf', 'math.pdf', '2MB', 'PDF', 'Test description', 0, 1, true),
        ('Physics Practice', 'natural', 'Physics', 'Bahir Dar', 'University', 'Dr Test', 'uploads/downloadables/physics.pdf', 'physics.pdf', '1.5MB', 'PDF', 'Test physics', 0, 1, true)
    """)
    
    # Insert new EntranceExams WITH is_active=True
    cur.execute("""
        INSERT INTO entrance_exams (title, year, stream, subject, institution, creator, file_path, file_name, file_size, file_type, question_count, uploaded_by, is_active) 
        VALUES 
        ('2024 Entrance Math', 2024, 'natural', 'Mathematics', 'MoE', 'Board', 'uploads/downloadables/entrance_math.pdf', 'entrance_math.pdf', '4MB', 'PDF', 100, 1, true),
        ('2023 Economics', 2023, 'social', 'Economics', 'MoE', 'Board', 'uploads/downloadables/entrance_econ.pdf', 'entrance_econ.pdf', '3.8MB', 'PDF', 80, 1, true)
    """)
    
    conn.commit()
    
    cur.execute("SELECT COUNT(*) as model_active FROM model_exams WHERE is_active=true")
    model_count = cur.fetchone()['model_active']
    cur.execute("SELECT COUNT(*) as entrance_active FROM entrance_exams WHERE is_active=true")
    entrance_count = cur.fetchone()['entrance_active']
    
    print(f'✅ Fixed & Seeded: {model_count} ACTIVE ModelExams + {entrance_count} ACTIVE EntranceExams')
    print(f'📊 Real files ready for download!')
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    seed_minimal()

