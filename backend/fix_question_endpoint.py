# Replace the CREATE QUESTION ENDPOINT section in app/routers/question_router.py with this code:

# CREATE QUESTION ENDPOINT
@router.post("/questions")
def create_question(question: dict, db: Session = Depends(get_db)):
    try:
        section_id = question.get("section_id")
        question_text = question.get("question_text")
        option_a = question.get("option_a")
        option_b = question.get("option_b")
        option_c = question.get("option_c")
        option_d = question.get("option_d")
        correct_answer = question.get("correct_answer")
        difficulty_input = question.get("difficulty", 2)
        marks = question.get("marks", 1)
        
        if not section_id or not question_text or not correct_answer:
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Convert difficulty to integer if needed (database expects Integer)
        if isinstance(difficulty_input, str):
            difficulty_map = {"Easy": 1, "Medium": 2, "Hard": 3}
            difficulty = difficulty_map.get(difficulty_input, 2)
        else:
            difficulty = difficulty_input
        
        new_question = question_models.QuestionModel(
            section_id=section_id,
            question_text=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            difficulty=difficulty,
            marks=marks
        )
        
        db.add(new_question)
        db.commit()
        db.refresh(new_question)
        
        return {"id": new_question.id, "message": "Question created successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
