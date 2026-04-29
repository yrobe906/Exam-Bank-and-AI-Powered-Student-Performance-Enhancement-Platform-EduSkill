# app/routers/ai_router.py
# AI Router for DeepSeek AI-powered recommendations
import os
import httpx
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from database import get_db
from app.models import exam_models, section_models, question_models, sector_models
from app.models.exam_attempt_models import ExamAttemptModel
from app.models.student_answer_models import StudentAnswerModel

load_dotenv()

router = APIRouter(prefix="/api/ai", tags=["AI Recommendations"])


class AIService:
    def __init__(self):
        # Using Groq - free API with no storage requirements
        self.api_key = os.getenv("GROQ_API_KEY", "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.base_url = "https://api.groq.com/openai/v1"
        print(f"DEBUG: Groq API Key loaded: {self.api_key[:10]}..." if self.api_key else "DEBUG: No API key found!")
    
    async def chat(self, message: str):
        """Simple AI chat function"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [{"role": "user", "content": message}],
                        "temperature": 0.7,
                        "max_tokens": 500
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return "I'm having trouble connecting to AI service. Status: " + str(response.status_code)
                    
        except Exception as e:
            return f"I encountered an error: {str(e)}. Please check your API key and internet connection."


ai_service = AIService()


# ==================== HELPER FUNCTIONS ====================

def get_questions_for_exam(db: Session, exam_id: int) -> List[Dict]:
    """Get all questions for a specific exam with section info"""
    sections = db.query(section_models.SectionModel).filter(
        section_models.SectionModel.exam_id == exam_id
    ).all()
    
    questions_data = []
    for section in sections:
        questions = db.query(question_models.QuestionModel).filter(
            question_models.QuestionModel.section_id == section.id
        ).all()
        
        for q in questions:
            questions_data.append({
                "id": q.id,
                "question_text": q.question_text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
                "correct_answer": q.correct_answer,
                "difficulty": q.difficulty,
                "marks": q.marks,
                "section_name": section.name,
                "section_id": section.id
            })
    
    return questions_data


def get_student_exam_answers(db: Session, student_id: int, exam_id: int) -> List[Dict]:
    """Get student's answers for a specific exam"""
    attempt = db.query(ExamAttemptModel).filter(
        ExamAttemptModel.student_id == student_id,
        ExamAttemptModel.exam_id == exam_id,
        ExamAttemptModel.completed_at != None
    ).order_by(ExamAttemptModel.id.desc()).first()
    
    if not attempt:
        return []
    
    answers = db.query(StudentAnswerModel).filter(
        StudentAnswerModel.attempt_id == attempt.id
    ).all()
    
    return [
        {
            "question_id": a.question_id,
            "selected_answer": a.selected_answer,
            "is_correct": a.is_correct
        }
        for a in answers
    ]


def get_difficulty_label(difficulty: int) -> str:
    """Convert difficulty number to label"""
    if difficulty == 1:
        return "Easy"
    elif difficulty == 2:
        return "Medium"
    elif difficulty == 3:
        return "Hard"
    return "Medium"


# ====================  AI RECOMMENDATIONS ====================

async def generate_deepseek_exam_recommendation(
    db: Session,
    student_id: int,
    exam_id: int
) -> Dict[str, Any]:
    """
    Generate AI-powered recommendation for an exam using DeepSeek AI.
    Analyzes the exam questions and student performance to provide personalized feedback.
    """
    # Get exam details
    exam = db.query(exam_models.ExamModel).filter(
        exam_models.ExamModel.id == exam_id
    ).first()
    
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # Ensure exam has a name
    exam_name = exam.name if exam.name else f"Exam {exam_id}"
    
    # Get sector/subject info
    sector = db.query(sector_models.SectorModel).filter(
        sector_models.SectorModel.id == exam.sector_id
    ).first()
    
    # Get questions
    questions = get_questions_for_exam(db, exam_id)
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found in this exam")
    
    # Get student answers
    student_answers = get_student_exam_answers(db, student_id, exam_id)
    
    # Create a map of student answers
    answers_map = {a["question_id"]: a for a in student_answers}
    
    # Calculate performance metrics
    total_questions = len(questions)
    correct_count = sum(1 for a in student_answers if a["is_correct"])
    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # Analyze questions by difficulty
    easy_count = sum(1 for q in questions if q["difficulty"] == 1)
    medium_count = sum(1 for q in questions if q["difficulty"] == 2)
    hard_count = sum(1 for q in questions if q["difficulty"] == 3)
    
    # Analyze by section with more detail
    section_analysis = {}
    question_patterns = {
        "calculation": ["calculate", "compute", "find", "solve", "what is"],
        "theory": ["explain", "describe", "what is", "define", "why"],
        "application": ["apply", "use", "how would", "in which"],
        "analysis": ["analyze", "compare", "contrast", "identify"]
    }
    
    for q in questions:
        section_name = q["section_name"]
        if section_name not in section_analysis:
            section_analysis[section_name] = {
                "total": 0,
                "correct": 0,
                "easy": 0,
                "medium": 0,
                "hard": 0,
                "question_types": {"calculation": 0, "theory": 0, "application": 0, "analysis": 0},
                "correct_types": {"calculation": 0, "theory": 0, "application": 0, "analysis": 0}
            }
        
        section_analysis[section_name]["total"] += 1
        
        # Add difficulty breakdown
        diff_label = get_difficulty_label(q["difficulty"]).lower()
        if diff_label in section_analysis[section_name]:
            section_analysis[section_name][diff_label] += 1
        
        # Analyze question type based on text
        question_text_lower = q["question_text"].lower()
        question_type = "theory"  # default
        for qtype, keywords in question_patterns.items():
            if any(keyword in question_text_lower for keyword in keywords):
                question_type = qtype
                break
        
        section_analysis[section_name]["question_types"][question_type] += 1
        
        # Check if student answered correctly
        if q["id"] in answers_map and answers_map[q["id"]]["is_correct"]:
            section_analysis[section_name]["correct"] += 1
            section_analysis[section_name]["correct_types"][question_type] += 1
    
    # Get student's historical performance in this sector
    sector_history = []
    if sector:
        # Get previous exams in same sector
        previous_attempts = db.query(ExamAttemptModel).join(exam_models.ExamModel).filter(
            ExamAttemptModel.student_id == student_id,
            exam_models.ExamModel.sector_id == sector.id,
            ExamAttemptModel.completed_at != None,
            ExamAttemptModel.exam_id != exam_id
        ).order_by(ExamAttemptModel.completed_at.desc()).limit(3).all()
        
        for attempt in previous_attempts:
            prev_exam = db.query(exam_models.ExamModel).filter(
                exam_models.ExamModel.id == attempt.exam_id
            ).first()
            if prev_exam:
                prev_answers = db.query(StudentAnswerModel).filter(
                    StudentAnswerModel.attempt_id == attempt.id
                ).all()
                prev_correct = sum(1 for a in prev_answers if a.is_correct)
                prev_total = len(prev_answers)
                prev_percentage = (prev_correct / prev_total * 100) if prev_total > 0 else 0
                sector_history.append({
                    "exam_name": prev_exam.name,
                    "score": prev_correct,
                    "total": prev_total,
                    "percentage": round(prev_percentage, 1)
                })
    
    # Build context for DeepSeek AI
    questions_sample = []
    for q in questions[:15]:  # Increased to 15 for better analysis
        student_answer = answers_map.get(q["id"], {})
        is_correct = student_answer.get("is_correct", None)
        selected = student_answer.get("selected_answer", "Not answered")
        
        # Determine question type
        question_text_lower = q["question_text"].lower()
        question_type = "theory"
        for qtype, keywords in question_patterns.items():
            if any(keyword in question_text_lower for keyword in keywords):
                question_type = qtype
                break
        
        questions_sample.append({
            "question": q["question_text"][:300],  # Increased truncation
            "difficulty": get_difficulty_label(q["difficulty"]),
            "section": q["section_name"],
            "type": question_type,
            "student_answer": selected,
            "is_correct": is_correct
        })
    
    # Ethiopian Grade 9-12 context - More detailed
    ethiopian_context = f"""
You are an expert AI tutor specializing in Ethiopian high school education (Grade 9-12). 
You understand the Ethiopian General Education curriculum, national exams, and teaching methodologies.

Subject-specific knowledge for {exam_name}:
- Focus on practical applications relevant to Ethiopian context
- Consider regional variations and cultural relevance
- Align with Ethiopian textbook content and exam patterns
- Address common misconceptions Ethiopian students face

Your recommendations should be:
- Highly specific to the student's performance patterns
- Progressive: build from current level to advanced concepts
- Actionable with specific study techniques for Ethiopian students
- Encouraging while being realistic about improvement needs
- Include Ethiopian curriculum references where relevant
- Suggest local resources and study methods when appropriate

For {exam_name}, emphasize:
- Core concepts that appear frequently in Ethiopian exams
- Problem-solving approaches used in Ethiopian classrooms
- Time management for Ethiopian exam conditions
- Building confidence through gradual mastery
"""
    
    # Create the prompt for DeepSeek
    prompt = f"""{ethiopian_context}

Analyze this Ethiopian Grade 9-12 student's exam performance in detail:

EXAM DETAILS:
- Exam Name: {exam_name}
- Subject Area: {sector.name if sector else 'Unknown'}
- Total Questions: {total_questions}
- Student's Score: {correct_count}/{total_questions} ({score_percentage:.1f}%)

PERFORMANCE BREAKDOWN:
- Easy Questions: {easy_count} total
- Medium Questions: {medium_count} total  
- Hard Questions: {hard_count} total

SECTION-BY-SECTION ANALYSIS:
{chr(10).join([f"- {sec}: {data['correct']}/{data['total']} correct ({data['easy']}E/{data['medium']}M/{data['hard']}H) | Types: Calc={data['question_types']['calculation']}, Theory={data['question_types']['theory']}, App={data['question_types']['application']}, Analysis={data['question_types']['analysis']}" for sec, data in section_analysis.items()])}

QUESTION TYPE PERFORMANCE:
{chr(10).join([f"- {sec}: Correct/Total - Calc: {data['correct_types']['calculation']}/{data['question_types']['calculation']}, Theory: {data['correct_types']['theory']}/{data['question_types']['theory']}, App: {data['correct_types']['application']}/{data['question_types']['application']}, Analysis: {data['correct_types']['analysis']}/{data['question_types']['analysis']}" for sec, data in section_analysis.items()])}

PREVIOUS PERFORMANCE IN THIS SUBJECT:
{chr(10).join([f"- {h['exam_name']}: {h['percentage']}%" for h in sector_history]) if sector_history else "No previous exams in this subject"}

SAMPLE QUESTIONS ANALYSIS (showing patterns):
{chr(10).join([f"Q: {q['question'][:150]}... | Type: {q['type']} | Diff: {q['difficulty']} | Section: {q['section']} | Answer: {q['student_answer']} | Correct: {q['is_correct']}" for q in questions_sample])}

Based on this comprehensive analysis, provide a detailed JSON response with:

1. "overall_assessment": Detailed 2-3 sentence analysis of performance, considering Ethiopian curriculum context
2. "strengths": List 3-4 specific areas where student excels - include both strong sections within this exam AND strong performance in the subject area based on historical data:
   - Format as "SubjectName: SectionName (score% correct)" for section strengths
   - Format as "SubjectName: Overall subject performance (avg% across X exams)" for subject strengths
   - Include improvement trends as "SubjectName: Showing improvement trend" if applicable
3. "areas_for_improvement": List 4-6 CRITICAL improvement recommendations in format "subject: section name". ONLY include sections/topics where the average score is below 50%:
   - Format each item as "SubjectName: SectionName (score% correct)"
   - Focus ONLY on sections with < 50% average performance within this exam
   - Include subject-level weaknesses as "SubjectName: Overall subject performance (avg% across X exams)" if historical performance shows <50% average
   - Address declining performance trends as "SubjectName: Declining performance trend (recent average X%)" if applicable
   - Provide concrete next steps for each weak area
   - If no sections are below 50%, focus on the lowest performing section
4. "detailed_feedback": Object with:
   - "question_type_analysis": Analysis of performance by calculation/theory/application/analysis
   - "difficulty_progression": How student handles easy→medium→hard progression
   - "sector_specific_insights": Insights specific to {exam_name} in Ethiopian context, including historical performance patterns
5. "recommendations": Array of 5-7 highly specific, actionable recommendations:
   - Include Ethiopian curriculum references
   - Suggest study techniques suitable for Ethiopian students
   - Address identified weaknesses directly
   - Build on identified strengths
   - Consider previous performance in the subject
6. "study_plan": 4-week study plan with weekly goals and specific activities
7. "next_exam_difficulty": Recommended difficulty level with justification
8. "encouragement": Personalized motivational message considering Ethiopian student context

Respond in JSON format only.
"""
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{ai_service.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {ai_service.api_key}",
                    "Content-Type": "application/json"
                },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    }
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data["choices"][0]["message"]["content"]
                
                # Try to parse JSON from response
                import json
                import re
                
                # Find JSON in response
                json_match = re.search(r'\{[\s\S]*\}', ai_response)
                if json_match:
                    try:
                        recommendation = json.loads(json_match.group())
                        return {
                            "success": True,
                            "exam_id": exam_id,
                            "exam_name": exam_name,
                            "subject": exam_name,
                            "score_percentage": round(score_percentage, 2),
                            "correct_answers": correct_count,
                            "total_questions": total_questions,
                            "sector_history": sector_history,
                            "recommendation": recommendation
                        }
                    except json.JSONDecodeError:
                        pass
                
                # If JSON parsing fails, return raw response
                return {
                    "success": True,
                    "exam_id": exam_id,
                    "exam_name": exam_name,
                    "subject": exam_name,
                    "score_percentage": round(score_percentage, 2),
                    "correct_answers": correct_count,
                    "total_questions": total_questions,
                    "sector_history": sector_history,
                    "recommendation": {
                        "overall_assessment": f"Scored {score_percentage:.1f}% in {sector.name if sector else 'this exam'} with specific patterns in question types and difficulty levels",
                        "strengths": ["Consistent performance in certain sections"],
                        "areas_for_improvement": [
                            "Dedicate extra time to practice calculation problems daily",
                            "Focus on understanding theoretical concepts before attempting applications",
                            "Work through easy questions first to build confidence, then progress to harder ones",
                            "Review incorrect answers immediately and understand the reasoning"
                        ],
                        "detailed_feedback": {
                            "question_type_analysis": "Analysis of calculation, theory, application, and analysis questions",
                            "difficulty_progression": f"Performance across easy/medium/hard questions: {easy_count}/{medium_count}/{hard_count}",
                            "sector_specific_insights": f"Performance in {sector.name if sector else 'this subject'} shows {'improvement' if sector_history else 'baseline'} patterns"
                        },
                        "recommendations": ["Practice more questions in weak areas", "Focus on specific question types", "Review Ethiopian curriculum materials"],
                        "study_plan": ["Week 1: Review basics", "Week 2: Practice weak areas", "Week 3: Mixed practice", "Week 4: Full mock exams"],
                        "next_exam_difficulty": "medium",
                        "encouragement": ai_response[:500]
                    }
                }
            else:
                # Print detailed error for debugging
                print(f"Groq API Error: Status {response.status_code}")
                print(f"Response: {response.text}")
                return {
                    "success": False,
                    "error": f"AI service returned status {response.status_code}. Response: {response.text[:200]}",
                    "fallback_recommendation": _generate_fallback_recommendation(score_percentage, section_analysis, question_patterns, sector_history, sector.name if sector else None, exam_name)
                }
                
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "fallback_recommendation": _generate_fallback_recommendation(score_percentage, section_analysis, question_patterns, sector_history, sector.name if sector else None, exam_name)
        }


def _generate_fallback_recommendation(score_percentage: float, section_analysis: Dict, question_patterns: Dict, sector_history: List = None, sector_name: str = None, exam_name: str = None) -> Dict:
    """Generate basic recommendation when AI is unavailable - analyzes sections and sector performance with < 50% threshold"""
    strengths = []
    areas_for_improvement = []
    
    # Analyze sections - ONLY sections with average score below 50% get improvement recommendations
    for section, data in section_analysis.items():
        if data["total"] > 0:
            section_score = (data["correct"] / data["total"]) * 100
            if section_score >= 70:
                strengths.append(f"Strong performance in {section} section ({section_score:.1f}% correct)")
            elif section_score < 50:
                # Format: "subject: section name"
                subject_display = exam_name if exam_name else (sector_name if sector_name else "this subject")
                areas_for_improvement.append(f"{subject_display}: {section} section ({section_score:.1f}% correct)")
    
    # Analyze sector-level performance if available - ONLY sectors with < 50% average
    if sector_history and sector_name:
        # Calculate sector average from history
        if sector_history:
            sector_avg = sum(h["percentage"] for h in sector_history) / len(sector_history)
            if sector_avg >= 70:
                strengths.append(f"Strong performance in {sector_name} subject (average {sector_avg:.1f}% across previous exams)")
            elif sector_avg < 50:
                areas_for_improvement.append(f"{sector_name}: Overall subject performance ({sector_avg:.1f}% average across {len(sector_history)} previous exams)")
        
        # Check for declining performance trends (additional concern even if above 50%)
        if len(sector_history) >= 2:
            recent_scores = [h["percentage"] for h in sector_history[:3]]  # Last 3 exams
            if len(recent_scores) >= 2:
                if recent_scores[0] > recent_scores[-1] + 5:
                    # Only add if the current trend is a concern (below 50% or declining significantly)
                    current_avg = sum(recent_scores) / len(recent_scores)
                    if current_avg < 50:
                        areas_for_improvement.append(f"{sector_name}: Declining performance trend (recent average {current_avg:.1f}%)")
    
    # If no sections are below 50%, but overall score is low, suggest the lowest performing section
    if not areas_for_improvement and score_percentage < 60:
        lowest_section = None
        lowest_score = 100
        for section, data in section_analysis.items():
            if data["total"] > 0:
                section_score = (data["correct"] / data["total"]) * 100
                if section_score < lowest_score:
                    lowest_score = section_score
                    lowest_section = section
        
        if lowest_section and lowest_score < 60:
            subject_display = exam_name if exam_name else (sector_name if sector_name else "this subject")
            areas_for_improvement.append(f"{subject_display}: {lowest_section} section ({lowest_score:.1f}% correct)")
    
    # Generate recommendations based on score
    recommendations = []
    if score_percentage >= 80:
        recommendations = [
            "Great job! Continue maintaining your performance",
            "Challenge yourself with harder questions",
            "Consider helping other students as a tutor"
        ]
        next_diff = "hard"
        encouragement = "Excellent work! You're mastering this subject!"
    elif score_percentage >= 60:
        recommendations = [
            "Good progress! Keep practicing regularly",
            "Focus on your weak areas identified above",
            "Try more medium-difficulty questions",
            "Review explanations for incorrect answers"
        ]
        next_diff = "medium"
        encouragement = "You're doing well! Keep up the consistent effort!"
    elif score_percentage >= 40:
        recommendations = [
            "Start with fundamentals - review basic concepts",
            "Practice easy questions to build confidence",
            "Gradually increase difficulty as you improve",
            "Don't hesitate to ask teachers for help"
        ]
        next_diff = "easy"
        encouragement = "Every expert was once a beginner. Keep practicing!"
    else:
        recommendations = [
            "Focus on understanding core concepts first",
            "Start with the easiest topics and master them",
            "Break down complex problems into smaller steps",
            "Use visual aids and practice examples"
        ]
        next_diff = "easy"
        encouragement = "Don't give up! Progress takes time. You've got this!"
    
    return {
        "overall_assessment": f"Scored {score_percentage:.1f}% - {'Keep improving!' if score_percentage >= 50 else 'Needs more practice'}",
        "strengths": strengths[:4] if strengths else ["Shows commitment to learning"],
        "areas_for_improvement": areas_for_improvement[:6] if areas_for_improvement else ["All sections performing adequately - focus on overall improvement"],
        "recommendations": recommendations,
        "next_exam_difficulty": next_diff,
        "encouragement": encouragement
    }


async def generate_deepseek_global_recommendation(
    db: Session,
    student_id: int
) -> Dict[str, Any]:
    """
    Generate global AI recommendation across all exams taken by the student.
    """
    from app.crud import analytics_crud
    
    # Get all exam attempts
    attempts = db.query(ExamAttemptModel).filter(
        ExamAttemptModel.student_id == student_id,
        ExamAttemptModel.completed_at != None
    ).order_by(ExamAttemptModel.completed_at.desc()).limit(10).all()
    
    if not attempts:
        return {
            "success": False,
            "error": "No completed exams found for this student"
        }
    
    # Get detailed performance by sector
    sector_performance = {}
    for attempt in attempts[:10]:  # Analyze last 10 exams
        exam = db.query(exam_models.ExamModel).filter(
            exam_models.ExamModel.id == attempt.exam_id
        ).first()
        
        if exam:
            sector = db.query(sector_models.SectorModel).filter(
                sector_models.SectorModel.id == exam.sector_id
            ).first()
            
            sector_name = sector.name if sector else "Unknown"
            if sector_name not in sector_performance:
                sector_performance[sector_name] = {
                    "exams_taken": 0,
                    "total_score": 0,
                    "best_score": 0,
                    "recent_scores": []
                }
            
            # Get score
            answers = db.query(StudentAnswerModel).filter(
                StudentAnswerModel.attempt_id == attempt.id
            ).all()
            
            correct = sum(1 for a in answers if a.is_correct)
            total = len(answers)
            percentage = (correct / total * 100) if total > 0 else 0
            
            sector_performance[sector_name]["exams_taken"] += 1
            sector_performance[sector_name]["total_score"] += percentage
            sector_performance[sector_name]["best_score"] = max(sector_performance[sector_name]["best_score"], percentage)
            sector_performance[sector_name]["recent_scores"].append(round(percentage, 1))
    
    # Calculate averages and trends
    for sector_name, data in sector_performance.items():
        data["average_score"] = round(data["total_score"] / data["exams_taken"], 1)
        data["recent_trend"] = "stable"
        if len(data["recent_scores"]) >= 3:
            recent_avg = sum(data["recent_scores"][-3:]) / 3
            earlier_avg = sum(data["recent_scores"][:-3]) / len(data["recent_scores"][:-3]) if data["recent_scores"][:-3] else recent_avg
            if recent_avg > earlier_avg + 5:
                data["recent_trend"] = "improving"
            elif recent_avg < earlier_avg - 5:
                data["recent_trend"] = "declining"
    
    # Ethiopian Grade 9-12 context
    ethiopian_context = """
You are an AI tutor specializing in Ethiopian high school education (Grade 9-12).
Your recommendations should be:
- Encouraging and supportive for students
- Progressive: start from easy concepts and gradually move to harder ones
- Aligned with Ethiopian national curriculum
- Practical and actionable for exam success
"""
    
    prompt = f"""{ethiopian_context}

Analyze this Ethiopian Grade 9-12 student's overall academic performance across all subjects:

OVERALL PERFORMANCE SUMMARY:
- Total exams completed: {total_exams}
- Subjects studied: {', '.join(sector_performance.keys())}
- Average score across all exams: {avg_score:.1f}%

SUBJECT-BY-SUBJECT ANALYSIS:
{chr(10).join([f"- {sector}: {data['exams_taken']} exams, Average: {data['average_score']}%, Best: {data['best_score']}%, Trend: {data['recent_trend']}" for sector, data in sector_performance.items()])}

DETAILED EXAM HISTORY:
{chr(10).join([f"- {e['exam_name']} ({e['subject']}): {e['percentage']}%" for e in recent_exams])}

Based on this comprehensive analysis of the student's Ethiopian high school journey, provide a detailed JSON response with:

1. "overall_assessment": Comprehensive 3-4 sentence analysis of learning progress and patterns
2. "strengths": List 3-5 subjects/areas where student consistently performs well
3. "weaknesses": List 3-5 subjects/areas needing significant improvement
4. "subject_specific_recommendations": Object mapping each subject to specific recommendations
5. "study_plan": Detailed 4-6 week study plan with:
   - Weekly focus areas
   - Specific activities for each subject
   - Time management suggestions
   - Ethiopian curriculum alignment
6. "exam_strategy": Recommendations for approaching Ethiopian national exams
7. "motivation": Encouraging message tailored to their performance patterns and Ethiopian student context

Respond in JSON format only.
"""
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{ai_service.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {ai_service.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data["choices"][0]["message"]["content"]
                
                import json
                import re
                
                json_match = re.search(r'\{[\s\S]*\}', ai_response)
                if json_match:
                    try:
                        recommendation = json.loads(json_match.group())
                        return {
                            "success": True,
                            "student_id": student_id,
                            "total_exams": total_exams,
                            "average_score": round(avg_score, 2),
                            "sector_performance": sector_performance,
                            "recent_exams": recent_exams,
                            "recommendation": recommendation
                        }
                    except json.JSONDecodeError:
                        pass
                
                return {
                    "success": True,
                    "student_id": student_id,
                    "total_exams": total_exams,
                    "average_score": round(avg_score, 2),
                    "sector_performance": sector_performance,
                    "recent_exams": recent_exams,
                    "recommendation": {
                        "overall_assessment": f"Completed {total_exams} exams across {len(sector_performance)} subjects with {avg_score:.1f}% average",
                        "strengths": ["Consistent practice across subjects"],
                        "weaknesses": ["Needs focused improvement in weak subjects"],
                        "subject_specific_recommendations": {sector: ["Practice regularly", "Review weak areas"] for sector in sector_performance.keys()},
                        "study_plan": ["Week 1: Assess all subjects", "Week 2-3: Focus on weaknesses", "Week 4: Comprehensive review"],
                        "exam_strategy": ["Practice time management", "Review past papers", "Focus on weak topics"],
                        "motivation": "Every step forward is progress!"
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"AI service returned status {response.status_code}"
                }
                
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==================== API ENDPOINTS ====================

@router.get("/health")
async def ai_health_check():
    """Health check for AI service"""
    return {
        "status": "ok",
        "message": "AI Router is working",
        "service": "DeepSeek AI",
        "endpoints": [
            "/ai/exam-recommendation/{student_id}/{exam_id}",
            "/ai/global-recommendation/{student_id}"
        ]
    }


@router.get("/exam-recommendation/{student_id}/{exam_id}")
async def get_exam_recommendation(
    student_id: int,
    exam_id: int,
    db: Session = Depends(get_db)
):
    """
    Get DeepSeek AI-powered recommendation for a specific exam.
    Analyzes exam questions and student performance to provide personalized feedback.
    """
    result = await generate_deepseek_exam_recommendation(db, student_id, exam_id)
    
    if not result.get("success", False) and "error" in result:
        # Check if it's a 404
        if "not found" in result["error"].lower():
            raise HTTPException(status_code=404, detail=result["error"])
        # Return with fallback
        return result
    
    return result


@router.get("/global-recommendation/{student_id}")
async def get_global_recommendation(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get global DeepSeek AI recommendation across all exams.
    Provides overall learning journey analysis and study plan.
    """
    result = await generate_deepseek_global_recommendation(db, student_id)
    
    if not result.get("success", False):
        if "not found" in result.get("error", "").lower():
            raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.post("/chat")
async def ai_chat(
    message: str,
    db: Session = Depends(get_db)
):
    """
    Simple AI chat endpoint for general questions.
    """
    response = await ai_service.chat(message)
    return {"response": response}
