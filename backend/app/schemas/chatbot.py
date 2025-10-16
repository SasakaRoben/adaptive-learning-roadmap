from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    context: Optional[dict] = None

class QuizRequest(BaseModel):
    topic_id: int
    num_questions: int = 5

class QuizResponse(BaseModel):
    questions: list
    topic_title: str