from typing import Optional, Dict

def get_user_by_username(cur, username: str) -> Optional[Dict]:
    """Get user by username"""
    cur.execute(
        "SELECT id, username, email, password_hash FROM users WHERE username = %s",
        (username,)
    )
    return cur.fetchone()

def get_user_by_email(cur, email: str) -> Optional[Dict]:
    """Get user by email"""
    cur.execute(
        "SELECT id, username, email, password_hash FROM users WHERE email = %s",
        (email,)
    )
    return cur.fetchone()