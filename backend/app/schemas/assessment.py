from pydantic import BaseModel
from typing import List, Optional

class AssessmentQuestion(BaseModel):
    id: int
    question_text: str
    question_type: str
    options: List[str]
    order_index: int

class AssessmentAnswer(BaseModel):
    question_id: int
    answer: str

class AssessmentSubmission(BaseModel):
    answers: List[AssessmentAnswer]

class AssessmentResult(BaseModel):
    score: int
    total_questions: int
    percentage: float
    assigned_level: str
    message: str
    next_steps: str