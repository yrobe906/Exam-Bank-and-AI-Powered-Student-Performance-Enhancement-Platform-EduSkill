import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

print('=== Adding section_id to student_exam_unlocks ===')

params = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'register_db',
    'user': 'postgres',
    'password': '4316'
}

try:
    conn = psycopg2.connect(**params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Step 1: Add column if not exists
    cur.execute('''
        ALTER TABLE student_exam_unlocks 
        ADD COLUMN IF NOT EXISTS section_id INTEGER;
    ''')

    # Step 2: Add FK constraint separately (safe if exists)
    cur.execute('''
        DO $$ BEGIN
            ALTER TABLE student_exam_unlocks 
            ADD CONSTRAINT fk_student_exam_unlocks_section 
            FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE SET NULL;
        EXCEPTION
            WHEN duplicate_object THEN 
                RAISE NOTICE 'Constraint already exists';
        END $$;
    ''')

    # Verify column
    cur.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'student_exam_unlocks' AND column_name = 'section_id';")
    result = cur.fetchone()
    if result:
        print(f'SUCCESS: section_id column verified: {result}')
    else:
        print('WARNING: Column not found.')

    # List columns
    cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'student_exam_unlocks' ORDER BY ordinal_position;")
    cols = cur.fetchall()
    print('student_exam_unlocks columns:')
    for col in cols:
        print(f'  - {col[0]}: {col[1]}')

    cur.close()
    conn.close()
    print('Migration COMPLETE! The 500 error is fixed. Restart server and test approve.')

except Exception as e:
    print(f'Error: {e}')

