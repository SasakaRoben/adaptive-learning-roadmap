from typing import List, Dict, Optional
import json

def get_assessment_questions(cur) -> List[Dict]:
    """Get all assessment questions"""
    cur.execute("""
        SELECT id, question_text, question_type, options, order_index
        FROM assessment_questions
        ORDER BY order_index
    """)
    return cur.fetchall()

def calculate_user_level(score: int, total_points: int) -> str:
    """Determine user level based on percentage of total points.
    score: accumulated points from correct answers
    total_points: maximum attainable points across all questions
    """
    if not total_points or total_points <= 0:
        # Fallback to beginner if misconfigured; caller should normally guard
        return "beginner"
    
    percentage = (score / total_points) * 100
    
    if percentage <= 40:
        return "beginner"
    elif percentage <= 70:
        return "intermediate"
    else:
        return "advanced"

def save_assessment_result(cur, user_id: int, score: int, total_questions: int, 
                           assigned_level: str, answers: List[Dict]):
    """Save user assessment result"""
    # Check if user already has assessment
    cur.execute("SELECT id FROM user_assessments WHERE user_id = %s", (user_id,))
    existing = cur.fetchone()
    
    if existing:
        # Update existing
        cur.execute("""
            UPDATE user_assessments
            SET score = %s, total_questions = %s, assigned_level = %s,
                answers = %s, completed_at = CURRENT_TIMESTAMP
            WHERE user_id = %s
        """, (score, total_questions, assigned_level, json.dumps(answers), user_id))
    else:
        # Insert new
        cur.execute("""
            INSERT INTO user_assessments (user_id, score, total_questions, assigned_level, answers)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, score, total_questions, assigned_level, json.dumps(answers)))
    
    # Update user's level and assessment status
    cur.execute("""
        UPDATE users
        SET current_level = %s, has_completed_assessment = TRUE
        WHERE id = %s
    """, (assigned_level, user_id))

def get_user_assessment(cur, user_id: int) -> Optional[Dict]:
    """Get user's assessment result"""
    cur.execute("""
        SELECT score, total_questions, assigned_level, completed_at
        FROM user_assessments
        WHERE user_id = %s
    """, (user_id,))
    return cur.fetchone()

def has_completed_assessment(cur, user_id: int) -> bool:
    """Check if user has completed assessment"""
    cur.execute("""
        SELECT has_completed_assessment
        FROM users
        WHERE id = %s
    """, (user_id,))
    result = cur.fetchone()
    return result['has_completed_assessment'] if result else False