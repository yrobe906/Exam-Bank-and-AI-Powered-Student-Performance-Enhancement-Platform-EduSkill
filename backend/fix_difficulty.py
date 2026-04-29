import re

with open('app/routers/question_router.py', 'r') as f:
    content = f.read()

# Replace the difficulty line
content = content.replace(
    'difficulty = question.get("difficulty", "Medium")',
    'difficulty_input = question.get("difficulty", 2)'
)

# Also need to add conversion logic
old_code = '''        if not section_id or not question_text or not correct_answer:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        new_question = question_models.QuestionModel('''

new_code = '''        if not section_id or not question_text or not correct_answer:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Convert difficulty to integer if needed (database expects Integer)
        if isinstance(difficulty_input, str):
            difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3}
            difficulty = difficulty_map.get(difficulty_input, 2)
        else:
            difficulty = difficulty_input
        
        new_question = question_models.QuestionModel('''

content = content.replace(old_code, new_code)

with open('app/routers/question_router.py', 'w') as f:
    f.write(content)

print('Fixed difficulty conversion')
