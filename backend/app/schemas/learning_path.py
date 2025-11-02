from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TopicResponse(BaseModel):
    id: int
    title: str
    description: str
    difficulty_level: str
    estimated_hours: float
    order_index: int
    level: str
    status: str  # 'locked', 'available', 'in_progress', 'completed'
    progress_percentage: float
    prerequisites: List[int]  # List of prerequisite topic IDs

class LearningPathResponse(BaseModel):
    user_level: str
    total_topics: int
    completed_topics: int
    in_progress_topics: int
    progress_percentage: float
    topics: List[TopicResponse]
    
class TopicDetailResponse(BaseModel):
    id: int
    title: str
    description: str
    content: str
    difficulty_level: str
    estimated_hours: float
    level: str
    status: str
    progress_percentage: float
    time_spent_minutes: int
    last_accessed: Optional[datetime]
    prerequisites: List[dict]  # List of prerequisite topics with details
    resources: List[dict]  # Learning resources

class StartTopicResponse(BaseModel):
    message: str
    topic_id: int
    status: str