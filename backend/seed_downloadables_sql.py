import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'register_db',
    'user': 'postgres',
    'password': '4316'  # From database.py
}

def seed_sql():
    conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    
    # Soft delete existing
    cur.execute("UPDATE model_exams SET is_active = false WHERE is_active = true")
    cur.execute("UPDATE entrance_exams SET is_active = false WHERE is_active = true")
    conn.commit()
    
    # Insert ModelExams
    model_exams = [
        (1, 'Grade 12 Math Model', 'natural', 'Mathematics', 'Jimma University', 'University', 'Prof Test', 'uploads/downloadables/math.pdf', 'math.pdf', '2MB', 'PDF', True, 1),
        (2, 'Physics Practice', 'natural', 'Physics', 'Bahir Dar', 'University', 'Dr Test', 'uploads/downloadables/physics.pdf', 'physics.pdf', '1.5MB', 'PDF', True, 1)
    ]
    cur.executemany("""
        INSERT INTO model_exams (id, title, stream, subject, institution, institution_type, creator, file_path, file_name, file_size, file_type, is_active, uploaded_by) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, model_exams)
    
    # Insert EntranceExams
    entrance_exams = [
        (1, '2024 Entrance Math', 2024, 'natural', 'Mathematics', 'MoE', 'Board', 'uploads/downloadables/entrance_math.pdf', 'entrance_math.pdf', '4MB', 'PDF', 100, None, True, 1),
        (2, '2023 Economics', 2023, 'social', 'Economics', 'MoE', 'Board', 'uploads/downloadables/entrance_econ.pdf', 'entrance_econ.pdf', '3.8MB', 'PDF', 80, None, True, 1)
    ]
    cur.executemany("""
        INSERT INTO entrance_exams (id, title, year, stream, subject, institution, creator, file_path, file_name, file_size, file_type, question_count, time_limit, is_active, uploaded_by) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, entrance_exams)
    
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM model_exams WHERE is_active=true")
    model_count = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) FROM entrance_exams WHERE is_active=true")
    entrance_count = cur.fetchone()['count']
    
    print(f'✅ SQL Seeded: {model_count} ModelExams + {entrance_count} EntranceExams')
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    seed_sql()

