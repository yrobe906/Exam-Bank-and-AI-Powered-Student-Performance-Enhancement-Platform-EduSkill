# analytics_crud.py
# CRUD operations for Analytics - Database queries and AI recommendation engine
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple

from app.models.analytics_models import (
    StudentSubjectAnalytics,
    StudentTopicAnalytics,
    StudentOverallAnalytics,
    StudentProgressHistory,
    AIRecommendation
)
from app.models.exam_models import ExamModel
from app.models.section_models import SectionModel
from app.models.sector_models import SectorModel
from app.models.exam_attempt_models import ExamAttemptModel
from app.models.student_answer_models import StudentAnswerModel
from app.models.question_models import QuestionModel
from app.models.flashcard_models import UserFlashcardProgress, Flashcard, FlashcardDeck
from app.models.practice_mock_models import PracticeMockAttempt, PracticeMockTest, PracticeQuestion
from app.models.user_models import User


# ==================== HELPER FUNCTIONS ====================

def get_db():
    """Get database session - will be overridden by router"""
    pass


def calculate_accuracy(correct: int, total: int) -> float:
    """Calculate accuracy percentage"""
    if total == 0:
        return 0.0
    return round((correct / total) * 100, 2)


def get_student_exam_attempts(db: Session, student_id: int, submitted_only: bool = False) -> List[ExamAttemptModel]:
    """
    Get exam attempts for a student.
    If submitted_only is True, only returns completed (submitted) exams.
    """
    query = db.query(ExamAttemptModel).filter(
        ExamAttemptModel.student_id == student_id
    )
    
    if submitted_only:
        query = query.filter(ExamAttemptModel.completed_at != None)
    
    return query.order_by(ExamAttemptModel.started_at).all()


def get_student_answers_for_exam(db: Session, attempt_id: int) -> List[StudentAnswerModel]:
    """Get all student answers for an exam attempt"""
    return db.query(StudentAnswerModel).filter(
        StudentAnswerModel.attempt_id == attempt_id
    ).all()


def get_section_from_question(db: Session, question_id: int) -> Optional[Tuple]:
    """Get section and sector info from question ID"""
    question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    if not question:
        return None
    
    section = db.query(SectionModel).filter(SectionModel.id == question.section_id).first()
    if not section:
        return None
    
    exam = db.query(ExamModel).filter(ExamModel.id == section.exam_id).first()
    if not exam:
        return None
    
    sector = db.query(SectorModel).filter(SectorModel.id == exam.sector_id).first()
    
    return section, exam, sector


# ==================== FLASHCARD ANALYTICS ====================

def get_flashcard_stats(db: Session, student_id: int) -> Dict:
    """
    Get flashcard progress statistics for a student.
    Returns detailed stats about flashcard practice.
    """
    # Import CardStatus locally to avoid issues
    from app.models.flashcard_models import CardStatus
    
    # Get all progress records for this student
    progress_records = db.query(UserFlashcardProgress).filter(
        UserFlashcardProgress.user_id == student_id
    ).all()
    
    if not progress_records:
        return {
            'total_cards_reviewed': 0,
            'learning_count': 0,
            'known_count': 0,
            'revisit_count': 0,
            'total_reviews': 0,
            'mastery_percentage': 0.0
        }
    
    learning_count = sum(1 for p in progress_records if p.status == CardStatus.LEARNING)
    known_count = sum(1 for p in progress_records if p.status == CardStatus.KNOWN)
    revisit_count = sum(1 for p in progress_records if p.status == CardStatus.REVISIT)
    total_reviews = sum(p.times_reviewed for p in progress_records)
    
    # Mastery = known cards / total cards reviewed
    total_cards = len(progress_records)
    mastery_percentage = round((known_count / total_cards * 100), 2) if total_cards > 0 else 0.0
    
    return {
        'total_cards_reviewed': total_cards,
        'learning_count': learning_count,
        'known_count': known_count,
        'revisit_count': revisit_count,
        'total_reviews': total_reviews,
        'mastery_percentage': mastery_percentage
    }


# ==================== PRACTICE MOCK ANALYTICS ====================

def get_practice_mock_stats(db: Session, student_id: int) -> Dict:
    """
    Get practice mock test statistics for a student.
    Returns detailed stats about practice test attempts.
    """
    # Get all completed practice mock attempts
    attempts = db.query(PracticeMockAttempt).filter(
        PracticeMockAttempt.student_id == student_id,
        PracticeMockAttempt.is_completed == True
    ).order_by(PracticeMockAttempt.started_at).all()
    
    if not attempts:
        return {
            'total_tests_taken': 0,
            'average_score': 0.0,
            'highest_score': 0.0,
            'lowest_score': 0.0,
            'total_questions_attempted': 0,
            'total_correct': 0,
            'subjects_practiced': []
        }
    
    scores = [a.percentage for a in attempts]
    total_questions = sum(a.total_questions for a in attempts)
    total_correct = sum(a.score for a in attempts)
    
    # Get unique subjects practiced
    subject_set = set()
    for attempt in attempts:
        mock_test = db.query(PracticeMockTest).filter(PracticeMockTest.id == attempt.mock_test_id).first()
        if mock_test:
            subject_set.add(mock_test.subject)
    
    return {
        'total_tests_taken': len(attempts),
        'average_score': round(sum(scores) / len(scores), 2) if scores else 0.0,
        'highest_score': max(scores) if scores else 0.0,
        'lowest_score': min(scores) if scores else 0.0,
        'total_questions_attempted': total_questions,
        'total_correct': total_correct,
        'subjects_practiced': list(subject_set)
    }


# ==================== ANALYTICS CALCULATION ====================

def calculate_subject_analytics(db: Session, student_id: int) -> Dict[int, Dict]:
    """
    Calculate subject-wise analytics for a student.
    Returns dict with sector_id as key and analytics data as value.
    Only counts SUBMITTED exams (where completed_at is not null).
    """
    # Get only submitted exam attempts
    attempts = get_student_exam_attempts(db, student_id, submitted_only=True)
    
    subject_data = {}  # sector_id -> analytics
    
    for attempt in attempts:
        # Get the exam and its sector
        exam = db.query(ExamModel).filter(ExamModel.id == attempt.exam_id).first()
        if not exam:
            continue
        
        sector_id = exam.sector_id
        
        # Initialize if not exists
        if sector_id not in subject_data:
            sector = db.query(SectorModel).filter(SectorModel.id == sector_id).first()
            subject_data[sector_id] = {
                'sector_id': sector_id,
                'sector_name': sector.name if sector else 'Unknown',
                'total_exams_taken': 0,
                'total_score': 0,
                'highest_score': 0,
                'lowest_score': 100,
                'total_questions': 0,
                'total_correct': 0,
            }
        
        # Get all answers for this attempt
        answers = get_student_answers_for_exam(db, attempt.id)
        
        subject_data[sector_id]['total_exams_taken'] += 1
        subject_data[sector_id]['total_score'] += attempt.score
        
        if attempt.score > subject_data[sector_id]['highest_score']:
            subject_data[sector_id]['highest_score'] = attempt.score
        if attempt.score < subject_data[sector_id]['lowest_score']:
            subject_data[sector_id]['lowest_score'] = attempt.score
        
        for answer in answers:
            subject_data[sector_id]['total_questions'] += 1
            if answer.is_correct:
                subject_data[sector_id]['total_correct'] += 1
    
    # Calculate averages
    for sector_id, data in subject_data.items():
        if data['total_exams_taken'] > 0:
            data['average_score'] = round(data['total_score'] / data['total_exams_taken'], 2)
        else:
            data['average_score'] = 0
        
        data['accuracy_percentage'] = calculate_accuracy(
            data['total_correct'], 
            data['total_questions']
        )
        
        # Handle lowest score if only one exam
        if data['total_exams_taken'] == 1:
            data['lowest_score'] = data['highest_score']
    
    return subject_data


def calculate_topic_analytics(db: Session, student_id: int) -> Dict[int, Dict]:
    """
    Calculate topic-wise analytics for a student.
    Returns dict with section_id as key and analytics data as value.
    Only counts SUBMITTED exams (where completed_at is not null).
    """
    # Get only submitted exam attempts
    attempts = get_student_exam_attempts(db, student_id, submitted_only=True)
    
    topic_data = {}  # section_id -> analytics
    
    for attempt in attempts:
        # Get all answers for this attempt
        answers = get_student_answers_for_exam(db, attempt.id)
        
        # Group answers by section
        section_scores = {}  # section_id -> {'total': 0, 'correct': 0, 'scores': []}
        
        for answer in answers:
            # Get section info from question
            question = db.query(QuestionModel).filter(QuestionModel.id == answer.question_id).first()
            if not question:
                continue
            
            section_id = question.section_id
            
            if section_id not in section_scores:
                section = db.query(SectionModel).filter(SectionModel.id == section_id).first()
                exam = db.query(ExamModel).filter(ExamModel.id == section.exam_id).first() if section else None
                sector = db.query(SectorModel).filter(SectorModel.id == exam.sector_id).first() if exam else None
                
                section_scores[section_id] = {
                    'section_id': section_id,
                    'section_name': section.name if section else 'Unknown',
                    'sector_id': exam.sector_id if exam else 0,
                    'sector_name': sector.name if sector else 'Unknown',
                    'total_questions': 0,
                    'total_correct': 0,
                    'exam_scores': [],
                }
            
            section_scores[section_id]['total_questions'] += 1
            if answer.is_correct:
                section_scores[section_id]['total_correct'] += 1
        
        # Calculate score per section (percentage of correct answers in this exam)
        for section_id, section_info in section_scores.items():
            score_pct = calculate_accuracy(
                section_info['total_correct'],
                section_info['total_questions']
            )
            section_info['exam_scores'].append(score_pct)
            
            # Initialize topic data
            if section_id not in topic_data:
                topic_data[section_id] = {
                    'section_id': section_id,
                    'section_name': section_info['section_name'],
                    'sector_id': section_info['sector_id'],
                    'sector_name': section_info['sector_name'],
                    'total_exams_taken': 0,
                    'total_score': 0,
                    'total_questions': 0,
                    'total_correct': 0,
                    'all_exam_scores': [],
                }
            
            topic_data[section_id]['total_exams_taken'] += 1
            topic_data[section_id]['total_score'] += score_pct
            topic_data[section_id]['total_questions'] += section_info['total_questions']
            topic_data[section_id]['total_correct'] += section_info['total_correct']
            topic_data[section_id]['all_exam_scores'].extend(section_info['exam_scores'])
    
    # Calculate averages and recent scores
    for section_id, data in topic_data.items():
        if data['total_exams_taken'] > 0:
            data['average_score'] = round(data['total_score'] / data['total_exams_taken'], 2)
        else:
            data['average_score'] = 0
        
        data['accuracy_percentage'] = calculate_accuracy(
            data['total_correct'],
            data['total_questions']
        )
        
        # Get last 5 exam scores for trend analysis
        data['recent_scores'] = data['all_exam_scores'][-5:] if len(data['all_exam_scores']) >= 5 else data['all_exam_scores']
        
        # Determine if weak topic and weakness level
        if data['total_exams_taken'] >= 3:
            if data['average_score'] < 50:
                data['is_weak_topic'] = True
                data['weakness_level'] = 3  # Severe
            elif data['average_score'] < 60:
                data['is_weak_topic'] = True
                data['weakness_level'] = 2  # Moderate
            elif data['average_score'] < 70:
                data['is_weak_topic'] = True
                data['weakness_level'] = 1  # Mild
            else:
                data['is_weak_topic'] = False
                data['weakness_level'] = 0
        else:
            data['is_weak_topic'] = False
            data['weakness_level'] = 0
    
    return topic_data


def calculate_overall_analytics(db: Session, student_id: int) -> Dict:
    """Calculate overall analytics for a student - only counts SUBMITTED exams"""
    subject_data = calculate_subject_analytics(db, student_id)
    topic_data = calculate_topic_analytics(db, student_id)
    
    all_scores = []
    total_exams = 0
    
    for sector_id, data in subject_data.items():
        total_exams += data['total_exams_taken']
        for _ in range(data['total_exams_taken']):
            # Approximate - we'd need actual exam scores
            pass
    
    # Get only submitted attempts and calculate percentage scores from actual answers
    attempts = get_student_exam_attempts(db, student_id, submitted_only=True)
    scores = []
    
    for attempt in attempts:
        # Get all answers for this attempt
        answers = get_student_answers_for_exam(db, attempt.id)
        if answers:
            # Calculate percentage from actual answers
            correct_count = sum(1 for a in answers if a.is_correct)
            percentage = (correct_count / len(answers)) * 100
            scores.append(percentage)
        else:
            # Fallback to stored score if no answers
            scores.append(attempt.score)
    
    if scores:
        average_score = sum(scores) / len(scores)
        highest_score = max(scores)
        lowest_score = min(scores)
    else:
        average_score = 0
        highest_score = 0
        lowest_score = 0
    
    weak_topics = [t for t in topic_data.values() if t.get('is_weak_topic', False)]
    
    return {
        'total_exams_taken': total_exams,
        'average_score': round(average_score, 2),
        'highest_score': highest_score,
        'lowest_score': lowest_score,
        'total_subjects_studied': len(subject_data),
        'total_topics_covered': len(topic_data),
        'weak_topics_count': len(weak_topics),
    }


# ==================== AI RECOMMENDATION ENGINE ====================

def analyze_trend(scores: List[float]) -> str:
    """Analyze trend from recent scores"""
    if len(scores) < 2:
        return "insufficient_data"
    
    # Compare first half average to second half average
    mid = len(scores) // 2
    first_half = scores[:mid]
    second_half = scores[mid:]
    
    first_avg = sum(first_half) / len(first_half)
    second_avg = sum(second_half) / len(second_half)
    
    diff = second_avg - first_avg
    
    if diff > 10:
        return "improving"
    elif diff < -10:
        return "declining"
    else:
        return "stagnant"


def generate_ai_recommendations(db: Session, student_id: int) -> List[Dict]:
    """
    AI Recommendation Engine - Rule-based AI logic
    
    Rules:
    1. Score < 50% in 3+ exams → Recommend materials
    2. Score 50-70% in 3+ exams → Recommend more practice
    3. Improving trend → Congratulate and suggest advanced topics
    4. Stagnant → Suggest different learning materials
    5. Time-based → If taking too long, suggest time management
    """
    recommendations = []
    topic_data = calculate_topic_analytics(db, student_id)
    
    for section_id, topic in topic_data.items():
        recent_scores = topic.get('recent_scores', [])
        
        if len(recent_scores) < 3:
            continue
        
        avg_score = topic['average_score']
        trend = analyze_trend(recent_scores)
        
        # Rule 1: Score < 50% in 3+ exams → Recommend materials
        if avg_score < 50:
            recommendations.append({
                'recommendation_type': 'weak_topic',
                'priority': 1,  # High
                'section_id': section_id,
                'sector_id': topic['sector_id'],
                'section_name': topic['section_name'],
                'sector_name': topic['sector_name'],
                'title': f'📚 Focus on {topic["section_name"]}',
                'description': f'Your average score in {topic["section_name"]} is {avg_score:.1f}% across {topic["total_exams_taken"]} exams. We recommend reviewing the fundamental materials before practicing more questions.',
                'trigger_data': {
                    'average_score': avg_score,
                    'exam_count': topic['total_exams_taken'],
                    'recent_scores': recent_scores
                }
            })
        
        # Rule 2: Score 50-70% in 3+ exams → Recommend more practice
        elif 50 <= avg_score < 70:
            recommendations.append({
                'recommendation_type': 'practice',
                'priority': 2,  # Medium
                'section_id': section_id,
                'sector_id': topic['sector_id'],
                'section_name': topic['section_name'],
                'sector_name': topic['sector_name'],
                'title': f'📝 Practice more {topic["section_name"]}',
                'description': f'Your score in {topic["section_name"]} is around {avg_score:.1f}%. More practice will help you improve to 70%+ and master this topic.',
                'trigger_data': {
                    'average_score': avg_score,
                    'exam_count': topic['total_exams_taken'],
                    'recent_scores': recent_scores
                }
            })
        
        # Rule 3: Improving trend → Suggest advanced topics
        if trend == 'improving' and avg_score >= 70:
            recommendations.append({
                'recommendation_type': 'advance',
                'priority': 3,  # Low
                'section_id': section_id,
                'sector_id': topic['sector_id'],
                'section_name': topic['section_name'],
                'sector_name': topic['sector_name'],
                'title': f'🚀 Great progress in {topic["section_name"]}!',
                'description': f"You're improving in {topic['section_name']}! Consider tackling more advanced problems or moving to the next topic.",
                'trigger_data': {
                    'trend': trend,
                    'average_score': avg_score
                }
            })
        
        # Rule 4: Stagnant → Suggest different approach
        elif trend == 'stagnant' and 50 <= avg_score < 80:
            recommendations.append({
                'recommendation_type': 'practice',
                'priority': 2,
                'section_id': section_id,
                'sector_id': topic['sector_id'],
                'section_name': topic['section_name'],
                'sector_name': topic['sector_name'],
                'title': f'💡 Try a different approach for {topic["section_name"]}',
                'description': f"Your scores in {topic['section_name']} have been steady. Try different study methods like spaced repetition or teaching the concept to someone else.",
                'trigger_data': {
                    'trend': trend,
                    'average_score': avg_score
                }
            })
        
        # Rule 5: Declining → Immediate attention
        elif trend == 'declining':
            recommendations.append({
                'recommendation_type': 'weak_topic',
                'priority': 1,
                'section_id': section_id,
                'sector_id': topic['sector_id'],
                'section_name': topic['section_name'],
                'sector_name': topic['sector_name'],
                'title': f'⚠️ Attention needed: {topic["section_name"]}',
                'description': f"Your performance in {topic['section_name']} has been declining. Consider reviewing the basics and getting some help.",
                'trigger_data': {
                    'trend': trend,
                    'average_score': avg_score,
                    'recent_scores': recent_scores
                }
            })
    
    # Sort by priority
    recommendations.sort(key=lambda x: x['priority'])
    
    # Limit to top 10 recommendations
    return recommendations[:10]


# ==================== DATABASE OPERATIONS ====================

def save_subject_analytics(db: Session, student_id: int, subject_data: Dict[int, Dict]):
    """Save or update subject analytics to database"""
    for sector_id, data in subject_data.items():
        # Check if exists
        existing = db.query(StudentSubjectAnalytics).filter(
            and_(
                StudentSubjectAnalytics.student_id == student_id,
                StudentSubjectAnalytics.sector_id == sector_id
            )
        ).first()
        
        if existing:
            # Update
            existing.total_exams_taken = data['total_exams_taken']
            existing.average_score = data['average_score']
            existing.highest_score = data['highest_score']
            existing.lowest_score = data['lowest_score']
            existing.total_questions_attempted = data['total_questions']
            existing.total_correct_answers = data['total_correct']
            existing.calculated_at = datetime.utcnow()
        else:
            # Create new
            new_subject = StudentSubjectAnalytics(
                student_id=student_id,
                sector_id=sector_id,
                sector_name=data['sector_name'],
                total_exams_taken=data['total_exams_taken'],
                average_score=data['average_score'],
                highest_score=data['highest_score'],
                lowest_score=data['lowest_score'],
                total_questions_attempted=data['total_questions'],
                total_correct_answers=data['total_correct'],
            )
            db.add(new_subject)
    
    db.commit()


def save_topic_analytics(db: Session, student_id: int, topic_data: Dict[int, Dict]):
    """Save or update topic analytics to database"""
    for section_id, data in topic_data.items():
        # Check if exists
        existing = db.query(StudentTopicAnalytics).filter(
            and_(
                StudentTopicAnalytics.student_id == student_id,
                StudentTopicAnalytics.section_id == section_id
            )
        ).first()
        
        if existing:
            # Update
            existing.total_exams_taken = data['total_exams_taken']
            existing.average_score = data['average_score']
            existing.total_questions_attempted = data['total_questions']
            existing.total_correct_answers = data['total_correct']
            existing.recent_scores = data['recent_scores']
            existing.is_weak_topic = 1 if data['is_weak_topic'] else 0
            existing.weakness_level = data['weakness_level']
            existing.calculated_at = datetime.utcnow()
        else:
            # Create new
            new_topic = StudentTopicAnalytics(
                student_id=student_id,
                sector_id=data['sector_id'],
                section_id=section_id,
                sector_name=data['sector_name'],
                section_name=data['section_name'],
                total_exams_taken=data['total_exams_taken'],
                average_score=data['average_score'],
                total_questions_attempted=data['total_questions'],
                total_correct_answers=data['total_correct'],
                recent_scores=data['recent_scores'],
                is_weak_topic=1 if data['is_weak_topic'] else 0,
                weakness_level=data['weakness_level'],
            )
            db.add(new_topic)
    
    db.commit()


def save_overall_analytics(db: Session, student_id: int, overall_data: Dict):
    """Save or update overall analytics to database"""
    existing = db.query(StudentOverallAnalytics).filter(
        StudentOverallAnalytics.student_id == student_id
    ).first()
    
    if existing:
        existing.total_exams_taken = overall_data['total_exams_taken']
        existing.average_score = overall_data['average_score']
        existing.highest_score = overall_data['highest_score']
        existing.lowest_score = overall_data['lowest_score']
        existing.total_subjects_studied = overall_data['total_subjects_studied']
        existing.total_topics_covered = overall_data['total_topics_covered']
        existing.weak_topics_count = overall_data['weak_topics_count']
        existing.calculated_at = datetime.utcnow()
    else:
        new_overall = StudentOverallAnalytics(
            student_id=student_id,
            total_exams_taken=overall_data['total_exams_taken'],
            average_score=overall_data['average_score'],
            highest_score=overall_data['highest_score'],
            lowest_score=overall_data['lowest_score'],
            total_subjects_studied=overall_data['total_subjects_studied'],
            total_topics_covered=overall_data['total_topics_covered'],
            weak_topics_count=overall_data['weak_topics_count'],
        )
        db.add(new_overall)
    
    db.commit()


def save_recommendations(db: Session, student_id: int, recommendations: List[Dict]):
    """Save AI recommendations to database"""
    # Delete old recommendations for this student
    db.query(AIRecommendation).filter(
        AIRecommendation.student_id == student_id
    ).delete()
    
    # Add new recommendations
    for rec in recommendations:
        new_rec = AIRecommendation(
            student_id=student_id,
            recommendation_type=rec['recommendation_type'],
            priority=rec['priority'],
            sector_id=rec.get('sector_id'),
            section_id=rec.get('section_id'),
            sector_name=rec.get('sector_name'),
            section_name=rec.get('section_name'),
            title=rec['title'],
            description=rec.get('description'),
            trigger_data=rec.get('trigger_data', {}),
        )
        db.add(new_rec)
    
    db.commit()


# ==================== PUBLIC API FUNCTIONS ====================

def calculate_all_analytics(db: Session, student_id: int, force_refresh: bool = False) -> Dict:
    """
    Calculate all analytics for a student.
    This is the main function to be called to update analytics.
    """
    # Check if we need to recalculate (unless force_refresh)
    if not force_refresh:
        existing = db.query(StudentOverallAnalytics).filter(
            StudentOverallAnalytics.student_id == student_id
        ).first()
        
        if existing:
            # Check if calculated in last hour
            time_diff = datetime.utcnow() - existing.calculated_at
            if time_diff.total_seconds() < 3600:  # Less than 1 hour
                # Return existing data
                return {
                    'success': True,
                    'message': 'Using cached analytics',
                    'calculated_at': existing.calculated_at
                }
    
    # Calculate new analytics
    subject_data = calculate_subject_analytics(db, student_id)
    topic_data = calculate_topic_analytics(db, student_id)
    overall_data = calculate_overall_analytics(db, student_id)
    recommendations = generate_ai_recommendations(db, student_id)
    
    # Save to database
    save_subject_analytics(db, student_id, subject_data)
    save_topic_analytics(db, student_id, topic_data)
    save_overall_analytics(db, student_id, overall_data)
    save_recommendations(db, student_id, recommendations)
    
    return {
        'success': True,
        'message': 'Analytics calculated successfully',
        'calculated_subjects': len(subject_data),
        'calculated_topics': len(topic_data),
        'recommendations_generated': len(recommendations),
        'calculated_at': datetime.utcnow()
    }


def get_dashboard_summary(db: Session, student_id: int) -> Dict:
    """Get complete dashboard summary for a student"""
    # Try to get cached data first
    overall = db.query(StudentOverallAnalytics).filter(
        StudentOverallAnalytics.student_id == student_id
    ).first()
    
    if not overall:
        # Calculate if not exists
        calculate_all_analytics(db, student_id, force_refresh=True)
        overall = db.query(StudentOverallAnalytics).filter(
            StudentOverallAnalytics.student_id == student_id
        ).first()
    
    # Get subjects
    subjects = db.query(StudentSubjectAnalytics).filter(
        StudentSubjectAnalytics.student_id == student_id
    ).all()
    
    # Get weak topics
    weak_topics = db.query(StudentTopicAnalytics).filter(
        and_(
            StudentTopicAnalytics.student_id == student_id,
            StudentTopicAnalytics.is_weak_topic == 1
        )
    ).order_by(StudentTopicAnalytics.average_score).limit(5).all()
    
    # Get recommendations
    recommendations = db.query(AIRecommendation).filter(
        AIRecommendation.student_id == student_id
    ).order_by(AIRecommendation.priority).limit(5).all()
    
    # Get recent progress (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    progress = db.query(StudentProgressHistory).filter(
        and_(
            StudentProgressHistory.student_id == student_id,
            StudentProgressHistory.date >= week_ago
        )
    ).order_by(StudentProgressHistory.date).all()
    
    return {
        'student_id': student_id,
        'average_score': overall.average_score if overall else 0,
        'total_exams_taken': overall.total_exams_taken if overall else 0,
        'weak_topics_count': overall.weak_topics_count if overall else 0,
        'class_rank': overall.class_rank if overall else None,
        'subjects': [
            {
                'sector_id': s.sector_id,
                'sector_name': s.sector_name,
                'total_exams_taken': s.total_exams_taken,
                'average_score': s.average_score,
                'highest_score': s.highest_score,
                'lowest_score': s.lowest_score,
                'total_questions_attempted': s.total_questions_attempted,
                'total_correct_answers': s.total_correct_answers,
                'accuracy_percentage': calculate_accuracy(s.total_correct_answers, s.total_questions_attempted)
            }
            for s in subjects
        ],
        'weak_topics': [
            {
                'section_id': t.section_id,
                'section_name': t.section_name,
                'sector_id': t.sector_id,
                'sector_name': t.sector_name,
                'average_score': t.average_score,
                'recent_scores': t.recent_scores or [],
                'weakness_level': t.weakness_level,
                'exam_count': t.total_exams_taken,
                'trend': analyze_trend(t.recent_scores or []),
            }
            for t in weak_topics
        ],
        'recent_recommendations': [
            {
                'recommendation_type': r.recommendation_type,
                'priority': r.priority,
                'title': r.title,
                'description': r.description,
                'section_name': r.section_name,
                'sector_name': r.sector_name,
            }
            for r in recommendations
        ],
        'weekly_progress': [
            {
                'date': p.date.strftime('%Y-%m-%d'),
                'exams_taken': p.exams_taken_today,
                'score': p.score_today,
                'questions_attempted': p.questions_attempted_today,
                'correct_answers': p.correct_answers_today,
                'accuracy': calculate_accuracy(p.correct_answers_today, p.questions_attempted_today),
                'study_time_minutes': p.study_time_minutes
            }
            for p in progress
        ],
        'flashcard_stats': get_flashcard_stats(db, student_id),
        'practice_mock_stats': get_practice_mock_stats(db, student_id)
    }


# ==================== GETTERS FOR API ====================

def get_subject_analytics(db: Session, student_id: int) -> List[StudentSubjectAnalytics]:
    """Get all subject analytics for a student"""
    return db.query(StudentSubjectAnalytics).filter(
        StudentSubjectAnalytics.student_id == student_id
    ).all()


def get_topic_analytics(db: Session, student_id: int) -> List[StudentTopicAnalytics]:
    """Get all topic analytics for a student"""
    return db.query(StudentTopicAnalytics).filter(
        StudentTopicAnalytics.student_id == student_id
    ).order_by(StudentTopicAnalytics.average_score).all()


def get_weak_topics(db: Session, student_id: int) -> List[StudentTopicAnalytics]:
    """Get weak topics for a student"""
    return db.query(StudentTopicAnalytics).filter(
        and_(
            StudentTopicAnalytics.student_id == student_id,
            StudentTopicAnalytics.is_weak_topic == 1
        )
    ).order_by(StudentTopicAnalytics.average_score).all()


def get_recommendations(db: Session, student_id: int) -> List[AIRecommendation]:
    """Get AI recommendations for a student"""
    return db.query(AIRecommendation).filter(
        AIRecommendation.student_id == student_id
    ).order_by(AIRecommendation.priority).all()


def get_progress_history(db: Session, student_id: int, days: int = 30) -> List[StudentProgressHistory]:
    """Get progress history for a student"""
    start_date = datetime.utcnow() - timedelta(days=days)
    return db.query(StudentProgressHistory).filter(
        and_(
            StudentProgressHistory.student_id == student_id,
            StudentProgressHistory.date >= start_date
        )
    ).order_by(StudentProgressHistory.date).all()


# ==================== CLASS RANK CALCULATION ====================

def calculate_class_rank(db: Session, student_id: int) -> Optional[int]:
    """
    Calculate class rank for a student based on their grade.
    Rank is calculated among students in the same grade who have taken exams.
    """
    # Get the student's grade
    student = db.query(User).filter(User.id == student_id).first()
    if not student:
        return None
    
    student_grade = student.grade
    if not student_grade:
        # If student doesn't have a grade, can't calculate rank
        return None
    
    # Get all students in the same grade who have exam attempts
    # First, get all unique student_ids with exam attempts in this grade
    students_with_attempts = db.query(
        ExamAttemptModel.student_id,
        User.grade
    ).join(
        User, ExamAttemptModel.student_id == User.id
    ).filter(
        User.grade == student_grade
    ).distinct().all()
    
    if not students_with_attempts:
        return None
    
    # Calculate average score for each student in the same grade
    student_averages = []
    for sid, grade in students_with_attempts:
        attempts = get_student_exam_attempts(db, sid)
        scores = []
        
        for attempt in attempts:
            answers = get_student_answers_for_exam(db, attempt.id)
            if answers:
                correct_count = sum(1 for a in answers if a.is_correct)
                percentage = (correct_count / len(answers)) * 100
                scores.append(percentage)
            else:
                scores.append(attempt.score)
        
        if scores:
            avg_score = sum(scores) / len(scores)
            student_averages.append((sid, avg_score))
    
    if not student_averages:
        return None
    
    # Sort by average score descending
    student_averages.sort(key=lambda x: x[1], reverse=True)
    
    # Find rank of current student
    for rank, (sid, avg) in enumerate(student_averages, 1):
        if sid == student_id:
            return rank
    
    return None


# ==================== SECTION-WISE ANALYTICS ====================

def get_section_wise_scores(db: Session, student_id: int) -> List[Dict]:
    """
    Get average score per section for a student.
    Returns list of sections with their average scores.
    """
    topic_analytics = get_topic_analytics(db, student_id)
    
    return [
        {
            'section_id': t.section_id,
            'section_name': t.section_name,
            'sector_id': t.sector_id,
            'sector_name': t.sector_name,
            'total_exams_taken': t.total_exams_taken,
            'average_score': t.average_score,
            'total_questions_attempted': t.total_questions_attempted,
            'total_correct_answers': t.total_correct_answers,
            'accuracy_percentage': calculate_accuracy(t.total_correct_answers, t.total_questions_attempted) if t.total_questions_attempted > 0 else 0.0,
            'is_weak': t.average_score < 50,
            'weakness_level': t.weakness_level
        }
        for t in topic_analytics
    ]


# ==================== EXAM-WISE SCORES ====================

def get_exam_wise_scores(db: Session, student_id: int) -> List[Dict]:
    """
    Get scores for each exam taken by the student.
    Returns detailed breakdown including section-wise scores.
    """
    attempts = get_student_exam_attempts(db, student_id)
    
    exam_scores = []
    for attempt in attempts:
        exam = db.query(ExamModel).filter(ExamModel.id == attempt.exam_id).first()
        if not exam:
            continue
        
        # Get all answers for this attempt
        answers = get_student_answers_for_exam(db, attempt.id)
        
        # Calculate section-wise breakdown
        section_breakdown = {}
        for answer in answers:
            question = db.query(QuestionModel).filter(QuestionModel.id == answer.question_id).first()
            if not question:
                continue
            
            section_id = question.section_id
            section = db.query(SectionModel).filter(SectionModel.id == section_id).first()
            
            if section_id not in section_breakdown:
                section_breakdown[section_id] = {
                    'section_id': section_id,
                    'section_name': section.name if section else 'Unknown',
                    'correct': 0,
                    'total': 0
                }
            
            section_breakdown[section_id]['total'] += 1
            if answer.is_correct:
                section_breakdown[section_id]['correct'] += 1
        
        # Calculate percentages
        for sec_id, sec_data in section_breakdown.items():
            sec_data['percentage'] = round((sec_data['correct'] / sec_data['total']) * 100, 2) if sec_data['total'] > 0 else 0
        
        # Get total questions for this exam
        total_questions = exam.total_questions or 0
        correct_answers = sum(1 for a in answers if a.is_correct)
        
        exam_scores.append({
            'attempt_id': attempt.id,
            'exam_id': exam.id,
            'exam_name': exam.name,
            'sector_id': exam.sector_id,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'percentage': round((correct_answers / total_questions) * 100, 2) if total_questions > 0 else 0,
            'section_breakdown': list(section_breakdown.values()),
            'completed_at': attempt.completed_at.strftime('%Y-%m-%d %H:%M:%S') if attempt.completed_at else None
        })
    
    return exam_scores


# ==================== PER-EXAM AI RECOMMENDATION ====================

def generate_per_exam_recommendation(db: Session, student_id: int, attempt_id: int) -> Dict:
    """
    Generate AI recommendation right after an exam is submitted.
    Analyzes the specific exam performance and provides immediate feedback.
    """
    # Get the attempt
    attempt = db.query(ExamAttemptModel).filter(
        ExamAttemptModel.id == attempt_id,
        ExamAttemptModel.student_id == student_id
    ).first()
    
    if not attempt:
        return {
            'exam_score': 0,
            'weak_sections': [],
            'recommended_exam': None,
            'recommended_difficulty': 'medium'
        }
    
    # Get exam details
    exam = db.query(ExamModel).filter(ExamModel.id == attempt.exam_id).first()
    
    # Get all answers
    answers = get_student_answers_for_exam(db, attempt_id)
    
    # Calculate total and correct
    total_questions = len(answers)
    correct_count = sum(1 for a in answers if a.is_correct)
    exam_score = round((correct_count / total_questions) * 100, 2) if total_questions > 0 else 0
    
    # Find weak sections (score < 50%)
    weak_sections = []
    section_scores = {}
    
    for answer in answers:
        question = db.query(QuestionModel).filter(QuestionModel.id == answer.question_id).first()
        if not question:
            continue
        
        section_id = question.section_id
        section = db.query(SectionModel).filter(SectionModel.id == section_id).first()
        
        if section_id not in section_scores:
            section_scores[section_id] = {
                'section_id': section_id,
                'section_name': section.name if section else 'Unknown',
                'correct': 0,
                'total': 0
            }
        
        section_scores[section_id]['total'] += 1
        if answer.is_correct:
            section_scores[section_id]['correct'] += 1
    
    # Calculate section percentages and find weak ones
    for sec_id, sec_data in section_scores.items():
        sec_score = round((sec_data['correct'] / sec_data['total']) * 100, 2) if sec_data['total'] > 0 else 0
        sec_data['percentage'] = sec_score
        
        if sec_score < 50:
            weak_sections.append({
                'section_id': sec_id,
                'section_name': sec_data['section_name'],
                'score': sec_score
            })
    
    # Determine recommended exam type
    recommended_exam = None
    recommended_difficulty = 'medium'
    
    if exam_score >= 80:
        # Strong performance - recommend harder exam
        recommended_exam = 'advanced_test'
        recommended_difficulty = 'hard'
    elif exam_score < 40:
        # Weak performance - recommend easier revision
        recommended_exam = 'revision_test'
        recommended_difficulty = 'easy'
    elif weak_sections:
        # Has weak sections - recommend section-focused exam
        recommended_exam = 'practice_test'
        recommended_difficulty = 'medium'
    
    return {
        'exam_score': exam_score,
        'weak_sections': weak_sections,
        'recommended_exam': recommended_exam,
        'recommended_difficulty': recommended_difficulty,
        'total_questions': total_questions,
        'correct_answers': correct_count,
        'exam_name': exam.name if exam else 'Unknown Exam'
    }


# ==================== GLOBAL AI RECOMMENDATION ====================

def generate_global_recommendation(db: Session, student_id: int) -> Dict:
    """
    Generate global AI recommendation based on all exams taken.
    Analyzes overall performance trends and provides comprehensive recommendations.
    """
    # Get topic analytics
    topic_data = calculate_topic_analytics(db, student_id)
    
    # Get overall analytics
    overall_data = calculate_overall_analytics(db, student_id)
    
    # Get recent exam scores (last 3)
    attempts = get_student_exam_attempts(db, student_id)
    recent_attempts = attempts[-3:] if len(attempts) >= 3 else attempts
    
    recent_scores = []
    for attempt in recent_attempts:
        answers = get_student_answers_for_exam(db, attempt.id)
        if answers:
            correct_count = sum(1 for a in answers if a.is_correct)
            percentage = (correct_count / len(answers)) * 100
            recent_scores.append(percentage)
    
    # Analyze score trend
    score_trend = 'stable'
    if len(recent_scores) >= 2:
        if recent_scores[-1] > recent_scores[0] + 10:
            score_trend = 'improving'
        elif recent_scores[-1] < recent_scores[0] - 10:
            score_trend = 'declining'
    
    # Find strong sections (score >= 75%)
    strong_sections = []
    for section_id, topic in topic_data.items():
        if topic['average_score'] >= 75:
            strong_sections.append({
                'section_id': section_id,
                'section_name': topic['section_name'],
                'score': topic['average_score']
            })
    
    # Find weak sections (score < 50%)
    weak_sections = []
    for section_id, topic in topic_data.items():
        if topic['average_score'] < 50:
            weak_sections.append({
                'section_id': section_id,
                'section_name': topic['section_name'],
                'score': topic['average_score']
            })
    
    # Determine overall recommendation
    recommendations = []
    
    if score_trend == 'declining':
        recommendations.append({
            'type': 'revision',
            'title': '📚 Time for Revision',
            'description': 'Your scores have been declining recently. We recommend taking a revision mock test to refresh your knowledge.'
        })
    
    if len(strong_sections) > 0:
        recommendations.append({
            'type': 'advance',
            'title': '🚀 Advanced Challenge',
            'description': f"You're strong in {strong_sections[0]['section_name']}! Consider taking an advanced test to challenge yourself further."
        })
    
    if len(weak_sections) >= 2:
        recommendations.append({
            'type': 'targeted_practice',
            'title': '🎯 Targeted Practice',
            'description': f"You have {len(weak_sections)} weak areas. We recommend focused practice exams to improve your performance."
        })
    
    if overall_data['average_score'] >= 70 and score_trend == 'stable':
        recommendations.append({
            'type': 'maintain',
            'title': '⭐ Keep It Up!',
            'description': 'You have a solid average score. Keep maintaining your performance!'
        })
    
    return {
        'overall_average': overall_data['average_score'],
        'total_exams': overall_data['total_exams_taken'],
        'score_trend': score_trend,
        'recent_scores': recent_scores,
        'strong_sections': strong_sections[:3],
        'weak_sections': weak_sections[:3],
        'recommendations': recommendations,
        'subjects_covered': overall_data['total_subjects_studied'],
        'topics_covered': overall_data['total_topics_covered']
    }


# ==================== ALL TOPICS PERFORMANCE TABLE ====================

def get_all_topics_performance(db: Session, student_id: int) -> List[Dict]:
    """
    Get all topics performance table data.
    Returns subject, topic, exams taken, avg result, and status.
    """
    topics = get_topic_analytics(db, student_id)
    
    performance_data = []
    for topic in topics:
        avg_result = topic.average_score
        
        # Determine status based on average
        if avg_result >= 75:
            status = 'Strong'
        elif avg_result >= 50:
            status = 'Moderate'
        else:
            status = 'Weak'
        
        performance_data.append({
            'subject': topic.sector_name,
            'topic': topic.section_name,
            'exams_taken': topic.total_exams_taken,
            'avg_result': round(avg_result, 2),
            'status': status
        })
    
    # Sort by average score ascending (weakest to strongest)
    performance_data.sort(key=lambda x: x['avg_result'])
    
    return performance_data


# ==================== RECALCULATE ALL STUDENTS ====================

def recalculate_all_students(db: Session) -> Dict:
    """
    Recalculate analytics for all students who have exam attempts.
    Returns summary of processing.
    """
    # Get all unique student_ids who have at least one exam attempt
    student_ids_with_attempts = db.query(
        ExamAttemptModel.student_id
    ).distinct().all()
    
    student_ids = [s[0] for s in student_ids_with_attempts]
    
    if not student_ids:
        return {
            'success': True,
            'message': 'No exam attempts found in the system',
            'students_processed': 0
        }
    
    results = []
    successful = 0
    
    for student_id in student_ids:
        try:
            # Check if student exists
            student = db.query(User).filter(User.id == student_id).first()
            if not student:
                continue
            
            # Calculate analytics with force refresh
            result = calculate_all_analytics(db, student_id, force_refresh=True)
            
            # Calculate class rank
            class_rank = calculate_class_rank(db, student_id)
            
            # Update class rank in overall analytics
            overall = db.query(StudentOverallAnalytics).filter(
                StudentOverallAnalytics.student_id == student_id
            ).first()
            if overall:
                overall.class_rank = class_rank
                db.commit()
            
            results.append({
                'student_id': student_id,
                'success': True,
                'class_rank': class_rank
            })
            successful += 1
            
        except Exception as e:
            results.append({
                'student_id': student_id,
                'success': False,
                'error': str(e)
            })
    
    return {
        'success': True,
        'message': f'Processed {successful}/{len(student_ids)} students',
        'students_processed': successful,
        'total_students': len(student_ids),
        'results': results
    }
