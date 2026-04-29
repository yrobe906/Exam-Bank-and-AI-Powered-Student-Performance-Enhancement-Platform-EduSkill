from database import SessionLocal
from app.crud import analytics_crud

db = SessionLocal()

# Test analytics calculation for student 1 (who has 33 exam attempts)
print("Calculating analytics for student 1...")
result = analytics_crud.calculate_all_analytics(db, student_id=1, force_refresh=True)
print(f"Result: {result}")

# Get the data
overall = db.query(analytics_crud.StudentOverallAnalytics).filter(
    analytics_crud.StudentOverallAnalytics.student_id == 1
).first()

if overall:
    print(f"\nOverall Analytics for Student 1:")
    print(f"  Total Exams Taken: {overall.total_exams_taken}")
    print(f"  Average Score: {overall.average_score}")
    print(f"  Highest Score: {overall.highest_score}")
    print(f"  Lowest Score: {overall.lowest_score}")
    print(f"  Subjects Studied: {overall.total_subjects_studied}")
    print(f"  Topics Covered: {overall.total_topics_covered}")
    print(f"  Weak Topics Count: {overall.weak_topics_count}")
else:
    print("No overall analytics found!")

# Get subjects
subjects = analytics_crud.get_subject_analytics(db, student_id=1)
print(f"\nSubject count: {len(subjects)}")
for s in subjects:
    print(f"  {s.sector_name}: {s.average_score}% ({s.total_exams_taken} exams)")

# Get topics
topics = analytics_crud.get_topic_analytics(db, student_id=1)
print(f"\nTopic count: {len(topics)}")
for t in topics[:5]:
    print(f"  {t.section_name}: {t.average_score}%")

db.close()
