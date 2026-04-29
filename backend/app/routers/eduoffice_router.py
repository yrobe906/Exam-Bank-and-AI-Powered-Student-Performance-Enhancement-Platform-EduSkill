from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from auth import get_current_eduoffice
from app.models.user_models import User
from app.models.exam_models import ExamModel
from app.models.exam_attempt_models import ExamAttemptModel
from app.models.analytics_models import StudentOverallAnalytics, StudentSubjectAnalytics, StudentTopicAnalytics

router = APIRouter(
    tags=["EduOffice"]
)


# ✅ 1. Get Dashboard Overview Stats for Education Office
@router.get("/dashboard-overview")
def get_dashboard_overview(
    current_user: User = Depends(get_current_eduoffice),
    db: Session = Depends(get_db)
):
    """
    Get overall dashboard statistics for Education Office:
    - Total registered students
    - Total registered teachers
    - Grade 12 readiness (average score)
    """

    # Total registered students (approved status)
    total_students = db.query(User).filter(
        User.role == "student",
        User.status == "approved"
    ).count()

    # Total registered teachers (approved status)
    total_teachers = db.query(User).filter(
        User.role == "teacher",
        User.status == "approved"
    ).count()

    # Total exams added
    total_exams = db.query(ExamModel).count()

    # Grade 12 readiness - average of average_score for grade 12 students
    grade_12_students = db.query(StudentOverallAnalytics).join(
        User, StudentOverallAnalytics.student_id == User.id
    ).filter(
        User.grade == 12,
        User.status == "approved"
    ).all()

    grade_12_readiness = 0.0
    if grade_12_students:
        total_score = sum(student.average_score for student in grade_12_students)
        grade_12_readiness = round(total_score / len(grade_12_students), 1)

    return {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_exams": total_exams,
        "grade_12_readiness": grade_12_readiness
    }


# ✅ 2. Get Grade-wise Performance for Education Office
@router.get("/grade-performance")
def get_grade_performance(
    current_user: User = Depends(get_current_eduoffice),
    db: Session = Depends(get_db)
):
    """
    Get performance metrics by grade (9, 10, 11, 12) for Education Office Dashboard.
    Returns:
    - total_students: Count of students in each grade
    - average_score: Average of all students' average scores in that grade
    - pass_rate: Percentage of students with average >= 50%
    """
    from app.models.exam_attempt_models import ExamAttemptModel
    from app.models.analytics_models import StudentOverallAnalytics

    grades = [9, 10, 11, 12]
    result = {}

    for grade in grades:
        # Get all users in this grade
        students_in_grade = db.query(User).filter(
            User.grade == grade,
            User.role == "student",
            User.status == "approved"
        ).all()

        total_students = len(students_in_grade)

        if total_students == 0:
            result[f"grade_{grade}"] = {
                "grade": grade,
                "total_students": 0,
                "average_score": 0,
                "pass_rate": 0
            }
            continue

        student_ids = [s.id for s in students_in_grade]

        # Get overall analytics for these students
        analytics_records = db.query(StudentOverallAnalytics).filter(
            StudentOverallAnalytics.student_id.in_(student_ids)
        ).all()

        if not analytics_records:
            # No analytics yet - try to calculate from exam attempts
            attempts = db.query(ExamAttemptModel).filter(
                ExamAttemptModel.student_id.in_(student_ids),
                ExamAttemptModel.completed_at != None
            ).all()

            if not attempts:
                result[f"grade_{grade}"] = {
                    "grade": grade,
                    "total_students": total_students,
                    "average_score": 0,
                    "pass_rate": 0
                }
                continue

            # Calculate average from exam attempts
            student_scores = {}
            for attempt in attempts:
                if attempt.student_id not in student_scores:
                    student_scores[attempt.student_id] = []
                student_scores[attempt.student_id].append(attempt.score)

            # Calculate average for each student
            all_averages = []
            passing_count = 0

            for sid, scores in student_scores.items():
                if scores:
                    student_avg = sum(scores) / len(scores)
                    all_averages.append(student_avg)
                    if student_avg >= 50:
                        passing_count += 1

            avg_score = sum(all_averages) / len(all_averages) if all_averages else 0
            pass_rate = (passing_count / len(all_averages) * 100) if all_averages else 0

            result[f"grade_{grade}"] = {
                "grade": grade,
                "total_students": total_students,
                "average_score": round(avg_score, 2),
                "pass_rate": round(pass_rate, 2)
            }
        else:
            # Use analytics data
            all_averages = [a.average_score for a in analytics_records if a.average_score is not None]
            passing_count = sum(1 for a in all_averages if a >= 50)

            avg_score = sum(all_averages) / len(all_averages) if all_averages else 0
            pass_rate = (passing_count / len(all_averages) * 100) if all_averages else 0

            result[f"grade_{grade}"] = {
                "grade": grade,
                "total_students": total_students,
                "average_score": round(avg_score, 2),
                "pass_rate": round(pass_rate, 2)
            }

    return result


# ✅ 3. Get Grade-wise Performance Distribution (for pie/doughnut chart)
@router.get("/grade-performance-distribution")
def get_grade_performance_distribution(
    current_user: User = Depends(get_current_eduoffice),
    db: Session = Depends(get_db)
):
    """
    Get performance distribution by grade for Education Office Dashboard.
    Categories:
    - top_performers: Average >= 85%
    - average: Average 50-85%
    - below_average: Average 40-50%
    - failing: Average < 40%
    """
    from app.models.analytics_models import StudentOverallAnalytics

    grades = [9, 10, 11, 12]
    result = {}

    for grade in grades:
        # Get all approved students in this grade
        students_in_grade = db.query(User).filter(
            User.grade == grade,
            User.role == "student",
            User.status == "approved"
        ).all()

        total_students = len(students_in_grade)

        if total_students == 0:
            result[f"grade_{grade}"] = {
                "grade": grade,
                "total_students": 0,
                "top_performers": 0,
                "average": 0,
                "below_average": 0,
                "failing": 0
            }
            continue

        student_ids = [s.id for s in students_in_grade]

        # Get overall analytics for these students
        analytics_records = db.query(StudentOverallAnalytics).filter(
            StudentOverallAnalytics.student_id.in_(student_ids)
        ).all()

        # Initialize counters
        top_performers = 0
        average = 0
        below_average = 0
        failing = 0

        if analytics_records:
            # Use analytics data
            for record in analytics_records:
                if record.average_score is None:
                    continue
                score = record.average_score
                if score >= 85:
                    top_performers += 1
                elif score >= 50:
                    average += 1
                elif score >= 40:
                    below_average += 1
                else:
                    failing += 1
        else:
            # Try to calculate from exam attempts
            from app.models.exam_attempt_models import ExamAttemptModel
            attempts = db.query(ExamAttemptModel).filter(
                ExamAttemptModel.student_id.in_(student_ids),
                ExamAttemptModel.completed_at != None
            ).all()

            if attempts:
                # Calculate average for each student
                student_scores = {}
                for attempt in attempts:
                    if attempt.student_id not in student_scores:
                        student_scores[attempt.student_id] = []
                    student_scores[attempt.student_id].append(attempt.score)

                for sid, scores in student_scores.items():
                    if scores:
                        student_avg = sum(scores) / len(scores)
                        if student_avg >= 85:
                            top_performers += 1
                        elif student_avg >= 50:
                            average += 1
                        elif student_avg >= 40:
                            below_average += 1
                        else:
                            failing += 1

        result[f"grade_{grade}"] = {
            "grade": grade,
            "total_students": total_students,
            "top_performers": top_performers,
            "average": average,
            "below_average": below_average,
            "failing": failing
        }

    return result