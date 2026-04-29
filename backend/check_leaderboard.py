# Create a test script that simulates exactly what happens in the API
# This will help us find the issue

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:4316@localhost:5432/register_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

print("=== SIMULATING EXACT API FLOW ===\n")

# Step 1: Get the teacher user (simulating token auth)
# In the real flow, the token gives us user_id=29
teacher_user_id = 29  # tade

result = db.execute(text(f"""
    SELECT id, username, full_name, role, status, teaching_grade
    FROM users 
    WHERE id = {teacher_user_id}
"""))
teacher = result.fetchone()
print(f"1. Current user from token: {teacher}")

if teacher:
    user_role = teacher[3]  # role
    teaching_grade = teacher[5]  # teaching_grade
    
    print(f"   Role: {user_role}")
    print(f"   Teaching Grade: {teaching_grade}")
    
    # Step 2: Determine grades to fetch
    if user_role == "teacher":
        if not teaching_grade:
            print("   ERROR: Teacher has no assigned grade!")
        else:
            grades_to_fetch = [teaching_grade]
            print(f"   Grades to fetch: {grades_to_fetch}")
            
            # Step 3: Execute the exact query from the API
            print(f"\n2. Executing student query...")
            
            # This is the EXACT query from user_router.py
            query = text("""
                SELECT u.id, u.full_name, u.username, u.profile_photo, u.grade, 
                       u.school_id, u.status, 
                       soa.average_score, soa.total_exams_taken
                FROM users u
                LEFT JOIN student_overall_analytics soa ON u.id = soa.student_id
                WHERE u.role = 'student' 
                  AND u.status = 'approved' 
                  AND u.grade = :grade
            """)
            
            result = db.execute(query, {"grade": teaching_grade})
            students = result.fetchall()
            
            print(f"   Found {len(students)} students")
            for s in students:
                print(f"   - {s}")
            
            # Step 4: Build response
            print(f"\n3. Building response...")
            
            result_list = []
            for student in students:
                avg_score = float(student[7]) if student[7] is not None else 0.0
                total_exams = int(student[8]) if student[8] is not None else 0
                
                result_list.append({
                    "id": student[0],
                    "full_name": student[1],
                    "username": student[2],
                    "profile_photo": student[3],
                    "grade": student[4],
                    "average_score": round(avg_score, 2),
                    "total_exams_taken": total_exams
                })
            
            # Sort
            result_list.sort(key=lambda x: (-x["average_score"], -x["total_exams_taken"]))
            
            # Assign ranks
            for idx, student in enumerate(result_list):
                student["rank"] = idx + 1
            
            print(f"   Final result: {result_list}")
            
    elif user_role == "eduoffice":
        print("   EduOffice role detected - would fetch grades 9-12")

db.close()

