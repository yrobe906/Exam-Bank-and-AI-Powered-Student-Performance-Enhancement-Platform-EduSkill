# Add this to app/routers/question_router.py after the router definition

# ================= CREATE QUESTION =================
@router.post("/questions", status_code=status.HTTP_201_CREATED)
def create_question(
    question: dict,
    db: Session = Depends(get_db)
):
    """Create a new question for a section"""
    try:
        section_id = question.get("section_id")
        question_text = question.get("question_text")
        option_a = question.get("option_a")
        option_b = question.get("option_b")
        option_c = question.get("option_c")
        option_d = question.get("option_d")
        correct_answer = question.get("correct_answer")
        difficulty = question.get("difficulty", "Medium")
        marks = question.get("marks", 1)
        
        if not section_id:
            raise HTTPException(status_code=400, detail="section_id is required")
        if not question_text:
            raise HTTPException(status_code=400, detail="question_text is required")
        if not option_a or not option_b:
            raise HTTPException(status_code=400, detail="option_a and option_b are required")
        if not correct_answer:
            raise HTTPException(status_code=400, detail="correct_answer is required")
        
        section = db.query(section_models.SectionModel).filter(
            section_models.SectionModel.id == section_id
        ).first()
        
        if not section:
            raise HTTPException(status_code=404, detail=f"Section with id {section_id} not found")
        
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
        
        return {
            "id": new_question.id,
            "section_id": new_question.section_id,
            "question_text": new_question.question_text,
            "message": "Question created successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating question: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create question: {str(e)}")
