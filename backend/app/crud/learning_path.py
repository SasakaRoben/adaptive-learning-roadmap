from typing import List, Dict, Optional

def get_user_level(cur, user_id: int) -> str:
    """Get user's assigned level"""
    cur.execute("SELECT current_level FROM users WHERE id = %s", (user_id,))
    result = cur.fetchone()
    return result['current_level'] if result else 'beginner'

def get_topics_by_level(cur, level: str) -> List[Dict]:
    """Get all topics for a specific level"""
    cur.execute("""
        SELECT id, title, description, content, difficulty_level, 
               estimated_hours, order_index, level
        FROM topics
        WHERE level = %s
        ORDER BY order_index
    """, (level,))
    return cur.fetchall()

def get_topic_prerequisites(cur, topic_id: int) -> List[int]:
    """Get prerequisite topic IDs for a topic"""
    cur.execute("""
        SELECT prerequisite_topic_id
        FROM topic_prerequisites
        WHERE topic_id = %s
    """, (topic_id,))
    return [row['prerequisite_topic_id'] for row in cur.fetchall()]

def get_user_progress_for_topic(cur, user_id: int, topic_id: int) -> Optional[Dict]:
    """Get user's progress for a specific topic"""
    cur.execute("""
        SELECT status, progress_percentage, time_spent_minutes, last_accessed
        FROM user_progress
        WHERE user_id = %s AND topic_id = %s
    """, (user_id, topic_id))
    return cur.fetchone()

def get_user_completed_topics(cur, user_id: int) -> List[int]:
    """Get list of completed topic IDs for a user"""
    cur.execute("""
        SELECT topic_id
        FROM user_progress
        WHERE user_id = %s AND status = 'completed'
    """, (user_id,))
    return [row['topic_id'] for row in cur.fetchall()]

def determine_topic_status(topic_id: int, prerequisites: List[int], 
                          completed_topics: List[int], user_progress: Optional[Dict]) -> str:
    """Determine if topic is locked, available, in_progress, or completed"""
    # If user has progress, return that status
    if user_progress:
        return user_progress['status']
    
    # Check if all prerequisites are completed
    if prerequisites:
        all_prereqs_completed = all(prereq in completed_topics for prereq in prerequisites)
        if not all_prereqs_completed:
            return 'locked'
    
    # No prerequisites or all completed
    return 'available'

def start_topic(cur, user_id: int, topic_id: int):
    """Mark a topic as started for a user"""
    cur.execute("""
        INSERT INTO user_progress (user_id, topic_id, status, last_accessed)
        VALUES (%s, %s, 'in_progress', CURRENT_TIMESTAMP)
        ON CONFLICT (user_id, topic_id) 
        DO UPDATE SET 
            status = 'in_progress',
            last_accessed = CURRENT_TIMESTAMP
    """, (user_id, topic_id))

def complete_topic(cur, user_id: int, topic_id: int):
    """Mark a topic as completed"""
    cur.execute("""
        UPDATE user_progress
        SET status = 'completed',
            progress_percentage = 100,
            completed_at = CURRENT_TIMESTAMP
        WHERE user_id = %s AND topic_id = %s
    """, (user_id, topic_id))

def update_topic_progress(cur, user_id: int, topic_id: int, progress: int, time_spent: int):
    """Update progress for a topic"""
    cur.execute("""
        UPDATE user_progress
        SET progress_percentage = %s,
            time_spent_minutes = time_spent_minutes + %s,
            last_accessed = CURRENT_TIMESTAMP
        WHERE user_id = %s AND topic_id = %s
    """, (progress, time_spent, user_id, topic_id))

def get_topic_detail(cur, topic_id: int) -> Optional[Dict]:
    """Get detailed information about a topic"""
    cur.execute("""
        SELECT id, title, description, content, difficulty_level,
               estimated_hours, level, order_index
        FROM topics
        WHERE id = %s
    """, (topic_id,))
    return cur.fetchone()

def get_prerequisite_details(cur, topic_id: int) -> List[Dict]:
    """Get detailed information about prerequisites"""
    cur.execute("""
        SELECT t.id, t.title, t.level
        FROM topics t
        INNER JOIN topic_prerequisites tp ON t.id = tp.prerequisite_topic_id
        WHERE tp.topic_id = %s
    """, (topic_id,))
    return cur.fetchall()

def get_topic_resources(cur, topic_id: int) -> List[Dict]:
    """Get learning resources for a topic"""
    cur.execute("""
        SELECT id, title, resource_url, resource_type, platform, duration_minutes
        FROM learning_resources
        WHERE topic_id = %s
        ORDER BY id
    """, (topic_id,))
    return cur.fetchall()

def get_topic_resources(cur, topic_id: int) -> List[Dict]:
    """Get learning resources for a topic"""
    cur.execute("""
        SELECT id, title, resource_url, resource_type, platform, duration_minutes
        FROM learning_resources
        WHERE topic_id = %s
        ORDER BY id
    """, (topic_id,))
    return cur.fetchall()