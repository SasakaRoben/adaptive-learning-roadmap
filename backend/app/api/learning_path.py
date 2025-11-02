from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from app.schemas.learning_path import (
    LearningPathResponse, TopicResponse, TopicDetailResponse, StartTopicResponse
)
from app.crud.learning_path import (
    get_user_level, get_topics_by_level, get_topic_prerequisites,
    get_user_progress_for_topic, get_user_completed_topics, determine_topic_status,
    start_topic, complete_topic, get_topic_detail, get_prerequisite_details, get_topic_resources
)
from app.core.dependencies import get_current_user
from app.core.database import get_db

router = APIRouter(
    prefix="/api/learning-path",
    tags=["learning-path"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=LearningPathResponse, summary="Get user's learning path")
async def get_learning_path(current_user: Dict = Depends(get_current_user)):
    """
    Get the personalized learning path for the current user.
    
    Returns all topics for the user's level with progress tracking.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Get user's level
            user_level = get_user_level(cur, current_user['id'])
            
            # Get all topics for this level
            topics = get_topics_by_level(cur, user_level)
            
            # Get user's completed topics
            completed_topics = get_user_completed_topics(cur, current_user['id'])
            
            # Build topic responses with status
            topic_responses = []
            total_topics = len(topics)
            completed_count = 0
            in_progress_count = 0
            
            for topic in topics:
                # Get prerequisites
                prerequisites = get_topic_prerequisites(cur, topic['id'])
                
                # Get user progress
                user_progress = get_user_progress_for_topic(cur, current_user['id'], topic['id'])
                
                # Determine status
                status = determine_topic_status(
                    topic['id'], 
                    prerequisites, 
                    completed_topics, 
                    user_progress
                )
                
                # Count progress
                if status == 'completed':
                    completed_count += 1
                elif status == 'in_progress':
                    in_progress_count += 1
                
                progress_percentage = float(user_progress['progress_percentage']) if user_progress else 0
                
                topic_responses.append(TopicResponse(
                    id=topic['id'],
                    title=topic['title'],
                    description=topic['description'],
                    difficulty_level=topic['difficulty_level'],
                    estimated_hours=float(topic['estimated_hours']),
                    order_index=topic['order_index'],
                    level=topic['level'],
                    status=status,
                    progress_percentage=progress_percentage,
                    prerequisites=prerequisites
                ))
            
            # Calculate overall progress
            overall_progress = (completed_count / total_topics * 100) if total_topics > 0 else 0
            
            return LearningPathResponse(
                user_level=user_level,
                total_topics=total_topics,
                completed_topics=completed_count,
                in_progress_topics=in_progress_count,
                progress_percentage=round(overall_progress, 2),
                topics=topic_responses
            )
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to load learning path: {str(e)}")

@router.get("/topics/{topic_id}", response_model=TopicDetailResponse, summary="Get topic details")
async def get_topic_details(topic_id: int, current_user: Dict = Depends(get_current_user)):
    """
    Get detailed information about a specific topic.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Get topic details
            topic = get_topic_detail(cur, topic_id)
            if not topic:
                raise HTTPException(status_code=404, detail="Topic not found")
            
            # Get user progress
            user_progress = get_user_progress_for_topic(cur, current_user['id'], topic_id)
            
            # Get prerequisites
            prerequisites = get_prerequisite_details(cur, topic_id)
            completed_topics = get_user_completed_topics(cur, current_user['id'])
            
            # Get resources
            resources = get_topic_resources(cur, topic_id)
            
            # Determine status
            prereq_ids = [p['id'] for p in prerequisites]
            status = determine_topic_status(topic_id, prereq_ids, completed_topics, user_progress)
            
            return TopicDetailResponse(
                id=topic['id'],
                title=topic['title'],
                description=topic['description'],
                content=topic['content'],
                difficulty_level=topic['difficulty_level'],
                estimated_hours=float(topic['estimated_hours']),
                level=topic['level'],
                status=status,
                progress_percentage=user_progress['progress_percentage'] if user_progress else 0,
                time_spent_minutes=user_progress['time_spent_minutes'] if user_progress else 0,
                last_accessed=user_progress['last_accessed'] if user_progress else None,
                prerequisites=[
                    {"id": p['id'], "title": p['title'], "level": p['level']} 
                    for p in prerequisites
                ],
                resources=[
                    {
                        "id": r['id'],
                        "title": r['title'],
                        "url": r['resource_url'],
                        "type": r['resource_type'],
                        "platform": r['platform'],
                        "duration": int(r['duration_minutes']) if r.get('duration_minutes') is not None else None
                    }
                    for r in resources
                ]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topics/{topic_id}/start", response_model=StartTopicResponse, summary="Start learning a topic")
async def start_learning_topic(topic_id: int, current_user: Dict = Depends(get_current_user)):
    """
    Mark a topic as started and track progress.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Check if topic exists
            topic = get_topic_detail(cur, topic_id)
            if not topic:
                raise HTTPException(status_code=404, detail="Topic not found")
            
            # Check prerequisites
            prerequisites = get_topic_prerequisites(cur, topic_id)
            completed_topics = get_user_completed_topics(cur, current_user['id'])
            
            if prerequisites:
                all_completed = all(prereq in completed_topics for prereq in prerequisites)
                if not all_completed:
                    raise HTTPException(
                        status_code=400, 
                        detail="Please complete prerequisite topics first"
                    )
            
            # Start the topic
            start_topic(cur, current_user['id'], topic_id)
            
            return StartTopicResponse(
                message=f"Started learning: {topic['title']}",
                topic_id=topic_id,
                status="in_progress"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/topics/{topic_id}/complete", summary="Mark topic as completed")
async def complete_learning_topic(topic_id: int, current_user: Dict = Depends(get_current_user)):
    """
    Mark a topic as completed.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Check if topic exists and user has started it
            user_progress = get_user_progress_for_topic(cur, current_user['id'], topic_id)
            if not user_progress:
                raise HTTPException(status_code=400, detail="Please start the topic first")
            
            # Complete the topic
            complete_topic(cur, current_user['id'], topic_id)
            
            return {"message": "Topic completed successfully", "topic_id": topic_id}
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))