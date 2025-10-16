from openai import OpenAI
from app.core.config import settings
from typing import Dict, Optional
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None

async def get_chatbot_response(message: str, user_context: Dict) -> str:
    """
    Get response from OpenAI chatbot with user context
    """
    if not client:
        return "Chatbot is not configured. Please add OPENAI_API_KEY to your environment."
    
    try:
        # Build context-aware system prompt
        system_prompt = f"""You are a friendly and helpful programming mentor for a learning platform focused on Full-Stack JavaScript Development.

Student Context:
- Level: {user_context.get('level', 'beginner')}
- Current Topic: {user_context.get('current_topic', 'None')}
- Topics Completed: {user_context.get('completed_count', 0)}/{user_context.get('total_count', 0)}
- Progress: {user_context.get('progress_percentage', 0)}%

Your role:
1. Answer programming questions clearly and concisely
2. Provide encouragement and motivation
3. Suggest next steps in their learning journey
4. Give code examples when relevant
5. Explain concepts at their skill level
6. Be supportive and positive

Keep responses concise (2-3 paragraphs max) unless asked for detailed explanations."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"[CHATBOT ERROR] {str(e)}")
        return f"Sorry, I'm having trouble responding right now. Error: {str(e)}"

async def generate_quiz(topic_title: str, topic_content: str, num_questions: int = 5) -> list:
    """
    Generate quiz questions for a topic using AI
    """
    if not client:
        return []
    
    try:
        prompt = f"""Generate {num_questions} multiple-choice quiz questions for the topic: "{topic_title}"

Topic content: {topic_content[:500]}

Format as JSON array with this structure:
[
  {{
    "question": "Question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Brief explanation"
  }}
]

Make questions practical and test understanding, not just memorization."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        # Parse JSON response
        questions_json = response.choices[0].message.content
        # Remove markdown code blocks if present
        if "```json" in questions_json:
            questions_json = questions_json.split("```json")[1].split("```")[0]
        elif "```" in questions_json:
            questions_json = questions_json.split("```")[1].split("```")[0]
        
        questions = json.loads(questions_json.strip())
        return questions
        
    except Exception as e:
        print(f"[QUIZ GENERATION ERROR] {str(e)}")
        return []