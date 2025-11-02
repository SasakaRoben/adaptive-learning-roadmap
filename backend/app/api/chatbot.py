from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from app.schemas.chatbot import ChatMessage, ChatResponse, QuizRequest, QuizResponse
from app.services.chatbot import get_chatbot_response, generate_quiz
from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.crud.learning_path import (
    get_user_level,
    get_user_completed_topics,
    get_topic_detail,
)

router = APIRouter(
    prefix="/api/chatbot",
    tags=["chatbot"],
    responses={404: {"description": "Not found"}},
)

@router.post("/ask", response_model=ChatResponse, summary="Ask the AI chatbot")
async def ask_chatbot(
    chat_message: ChatMessage,
    current_user: Dict = Depends(get_current_user)
):
    """
    Send a message to the AI learning assistant.
    
    The chatbot has context about:
    - Your current level (beginner/intermediate/advanced)
    - Topics you've completed
    - Your current progress
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Get user context
            user_level = get_user_level(cur, current_user['id'])
            completed_topics = get_user_completed_topics(cur, current_user['id'])
            
            # Get total topics for level
            cur.execute(
                "SELECT COUNT(*) as total FROM topics WHERE level = %s",
                (user_level,)
            )
            total = cur.fetchone()['total']
            
            # Get current topic (last accessed)
            cur.execute("""
                SELECT t.title
                FROM user_progress up
                JOIN topics t ON up.topic_id = t.id
                WHERE up.user_id = %s AND up.status = 'in_progress'
                ORDER BY up.last_accessed DESC
                LIMIT 1
            """, (current_user['id'],))
            
            current_topic_row = cur.fetchone()
            current_topic = current_topic_row['title'] if current_topic_row else 'None'
            
            # Build context
            user_context = {
                'level': user_level,
                'current_topic': current_topic,
                'completed_count': len(completed_topics),
                'total_count': total,
                'progress_percentage': round((len(completed_topics) / total * 100), 2) if total > 0 else 0
            }
            
            # Get AI response
            response_text = await get_chatbot_response(chat_message.message, user_context)
            
            return ChatResponse(
                response=response_text,
                context=user_context
            )
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@router.post("/quiz", response_model=QuizResponse, summary="Generate quiz for a topic")
async def generate_topic_quiz(
    quiz_request: QuizRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Generate AI-powered quiz questions for a specific topic.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Get topic details
            topic = get_topic_detail(cur, quiz_request.topic_id)
            if not topic:
                raise HTTPException(status_code=404, detail="Topic not found")
            
            # Generate quiz questions
            questions = await generate_quiz(
                topic['title'],
                topic['content'],
                quiz_request.num_questions
            )
            
            if not questions:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to generate quiz questions"
                )
            
            return QuizResponse(
                questions=questions,
                topic_title=topic['title']
            )
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))