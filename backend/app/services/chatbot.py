from typing import Dict
import json
import asyncio
import logging
import google.generativeai as genai
from app.core.config import settings


_gemini_configured = False
_model = None
logger = logging.getLogger(__name__)

def _ensure_gemini_initialized():
    global _gemini_configured, _model
    if _gemini_configured:
        return
    if not settings.GEMINI_API_KEY:
        _gemini_configured = True
        return
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model_name = settings.GEMINI_MODEL or "gemini-1.5-flash"
    # Use system instruction to steer style and role
    _model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 800,
        },
    )
    _gemini_configured = True


def _call_generate(prompt: str):
    # Helper to call blocking SDK in a thread
    return _model.generate_content(prompt)


async def get_chatbot_response(message: str, user_context: Dict) -> str:
    """Get response from Gemini with user context."""
    _ensure_gemini_initialized()
    if not _model:
        return "Chatbot is not configured. Please add GEMINI_API_KEY to your environment."

    try:
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

        # Combine system prompt and user message into a single content
        full_prompt = f"{system_prompt}\n\nUser: {message}"
        # Run blocking call in a thread to avoid blocking the event loop
        loop = asyncio.get_running_loop()
        resp = await loop.run_in_executor(None, _call_generate, full_prompt)
        return (resp.text or "") if resp else ""
    except Exception as e:
        logger.error(f"[CHATBOT ERROR] {str(e)}", exc_info=True)
        return "Sorry, I'm having trouble responding right now."


async def generate_quiz(topic_title: str, topic_content: str, num_questions: int = 5) -> list:
    """Generate quiz questions for a topic using Gemini."""
    _ensure_gemini_initialized()
    if not _model:
        return []

    try:
        prompt = f"""Generate {num_questions} multiple-choice quiz questions for the topic: "{topic_title}"

Topic content: {topic_content[:500]}

Return ONLY valid JSON (no markdown) as an array with this exact structure:
[
  {{
    "question": "Question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Brief explanation"
  }}
]

Ensure each question has exactly 4 options and one correct_answer matching one of the options.
"""

        loop = asyncio.get_running_loop()
        resp = await loop.run_in_executor(None, _call_generate, prompt)
        questions_json = resp.text if resp else "[]"
        # Remove markdown fences if any
        if "```json" in questions_json:
            questions_json = questions_json.split("```json")[1].split("```")[0]
        elif "```" in questions_json:
            questions_json = questions_json.split("```")[1].split("```")[0]

        questions = json.loads(questions_json.strip())

        # Basic normalization
        normalized = []
        for q in questions:
            opts = q.get("options") or []
            if not isinstance(opts, list):
                continue
            # Ensure exactly 4 options if possible
            if len(opts) < 4:
                # Pad with plausible distractors
                opts = opts + [f"Option {chr(65+i)}" for i in range(len(opts), 4)]
            elif len(opts) > 4:
                opts = opts[:4]
            ca = q.get("correct_answer")
            if ca not in opts and opts:
                ca = opts[0]
            normalized.append({
                "question": q.get("question", ""),
                "options": opts,
                "correct_answer": ca,
                "explanation": q.get("explanation", "")
            })

        return normalized
    except Exception as e:
        logger.error(f"[QUIZ GENERATION ERROR] {str(e)}", exc_info=True)
        return []