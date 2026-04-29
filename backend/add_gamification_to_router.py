import re

# Read the file
with open('app/routers/question_router.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the return statement section
old_code = '''            if deepseek_recommendation:
                ai_recommendation = deepseek_recommendation.get('recommendation') or deepseek_recommendation

        return {'''

new_code = '''            if deepseek_recommendation:
                ai_recommendation = deepseek_recommendation.get('recommendation') or deepseek_recommendation

        # ==================== GAMIFICATION: Award XP ====================
        xp_earned = 0
        xp_breakdown = {}
        
        try:
            gamification_service = get_gamification_service(db)
            
            # Award XP for exam submission (20 XP)
            submission_xp = gamification_service.award_exam_submission_xp(student_id, attempt.exam_id)
            if submission_xp:
                xp_earned += submission_xp.xp_amount
                xp_breakdown['submission'] = submission_xp.xp_amount
                gamification_service.add_cooldown(student_id, 'exam_submission', attempt.exam_id)
            
            # Award XP for exam result based on percentage
            result_xp = gamification_service.award_exam_result_xp(student_id, attempt.exam_id, percentage)
            if result_xp:
                xp_earned += result_xp.xp_amount
                xp_breakdown['result'] = result_xp.xp_amount
            
            # Record activity for streak tracking
            gamification_service.record_activity(
                user_id=student_id,
                activity_type='exam_attempt',
                content_id=attempt.exam_id,
                content_type='exam',
                completion_percentage=100.0
            )
            
            print(f'Gamification XP awarded: {xp_earned} XP (breakdown: {xp_breakdown})')
            
        except Exception as gamification_error:
            print(f'WARNING: Failed to award gamification XP: {str(gamification_error)}')

        return {'''

if old_code in content:
    content = content.replace(old_code, new_code)
    
    # Also update the return dict to include xp info
    old_return = '''            "message": "Exam submitted successfully",
            "ai_recommendation": ai_recommendation
        }'''
    
    new_return = '''            "message": "Exam submitted successfully",
            "ai_recommendation": ai_recommendation,
            "xp_earned": xp_earned,
            "xp_breakdown": xp_breakdown
        }'''
    
    content = content.replace(old_return, new_return)
    
    with open('app/routers/question_router.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: Gamification integration added to question_router.py')
else:
    print('ERROR: Could not find the target code section')
