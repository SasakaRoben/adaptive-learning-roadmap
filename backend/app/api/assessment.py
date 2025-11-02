from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from app.schemas.assessment import (
    AssessmentQuestion, AssessmentSubmission, AssessmentResult
)
from app.crud.assessment import (
    get_assessment_questions, calculate_user_level, 
    save_assessment_result, get_user_assessment, has_completed_assessment
)
from app.core.dependencies import get_current_user
from app.core.database import get_db

router = APIRouter(
    prefix="/api/assessment",
    tags=["assessment"],
    responses={404: {"description": "Not found"}},
)

@router.get("/questions", response_model=List[AssessmentQuestion], summary="Get assessment questions")
async def get_questions(current_user: Dict = Depends(get_current_user)):
    """
    Get all assessment questions for skill evaluation.
    
    Returns a list of questions to determine user's programming level.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            questions = get_assessment_questions(cur)
            
            # Don't include correct answers in response
            return [
                {
                    "id": q['id'],
                    "question_text": q['question_text'],
                    "question_type": q['question_type'],
                    # Ensure options is always a list for the schema
                    "options": q['options'] or [],
                    "order_index": q['order_index']
                }
                for q in questions
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch questions: {str(e)}")

@router.post("/submit", response_model=AssessmentResult, summary="Submit assessment answers")
async def submit_assessment(
    submission: AssessmentSubmission,
    current_user: Dict = Depends(get_current_user)
):
    """
    Submit assessment answers and get assigned level.
    
    Evaluates user's answers and assigns them to beginner, intermediate, or advanced path.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Get all questions with correct answers
            questions = get_assessment_questions(cur)
            
            # Calculate score
            score = 0
            total_questions = len(questions)
            
            # Create answer map
            answer_map = {ans.question_id: ans.answer for ans in submission.answers}
            
            # Get correct answers
            cur.execute("SELECT id, correct_answer, points FROM assessment_questions")
            correct_answers = {row['id']: row for row in cur.fetchall()}
            
            # Compute maximum possible points (handles variable point weights)
            max_points = sum((row.get('points') or 0) for row in correct_answers.values())
            
            if total_questions == 0 or max_points == 0:
                raise HTTPException(status_code=400, detail="No assessment questions available")
            
            # Score answers
            for q_id, user_answer in answer_map.items():
                if q_id in correct_answers:
                    if user_answer == correct_answers[q_id]['correct_answer']:
                        score += correct_answers[q_id]['points']
            
            # Determine level
            assigned_level = calculate_user_level(score, max_points)
            
            # Save result
            answers_data = [
                {"question_id": ans.question_id, "answer": ans.answer}
                for ans in submission.answers
            ]
            save_assessment_result(cur, current_user['id'], score, total_questions, assigned_level, answers_data)
            
            # Generate response message
            percentage = (score / max_points) * 100
            
            level_messages = {
                "beginner": {
                    "message": "Welcome to your learning journey! You'll start with the fundamentals.",
                    "next_steps": "Begin with HTML, CSS, and JavaScript basics to build a strong foundation."
                },
                "intermediate": {
                    "message": "Great! You have some experience. Let's take you to the next level.",
                    "next_steps": "You'll dive into React, Node.js, and build full-stack applications."
                },
                "advanced": {
                    "message": "Impressive! You're ready for advanced concepts.",
                    "next_steps": "Focus on system design, performance optimization, and production-ready applications."
                }
            }
            
            return AssessmentResult(
                score=score,
                total_questions=total_questions,
                percentage=round(percentage, 2),
                assigned_level=assigned_level,
                message=level_messages[assigned_level]["message"],
                next_steps=level_messages[assigned_level]["next_steps"]
            )
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to submit assessment: {str(e)}")

@router.get("/status", summary="Check assessment status")
async def get_assessment_status(current_user: Dict = Depends(get_current_user)):
    """
    Check if user has completed the assessment.
    
    Returns assessment status and results if completed.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            completed = has_completed_assessment(cur, current_user['id'])
            
            if completed:
                result = get_user_assessment(cur, current_user['id'])
                return {
                    "completed": True,
                    "assigned_level": result['assigned_level'],
                    "score": result['score'],
                    "total_questions": result['total_questions'],
                    "completed_at": result['completed_at']
                }
            else:
                return {
                    "completed": False,
                    "assigned_level": None
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retake", summary="Retake assessment")
async def retake_assessment(current_user: Dict = Depends(get_current_user)):
    """
    Allow user to retake the assessment to change their level.
    
    Resets assessment status so user can take it again.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Mark assessment as not completed
            cur.execute("""
                UPDATE users
                SET has_completed_assessment = FALSE
                WHERE id = %s
            """, (current_user['id'],))
            
            return {"message": "You can now retake the assessment"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))