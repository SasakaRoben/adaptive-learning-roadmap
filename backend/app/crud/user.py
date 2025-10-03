from app.schemas.user import UserRegister
from app.core.security import hash_password
from typing import Optional, Dict

def check_username_exists(cur, username: str) -> bool:
    """Check if username already exists"""
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    return cur.fetchone() is not None

def check_email_exists(cur, email: str) -> bool:
    """Check if email already exists"""
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    return cur.fetchone() is not None

def create_user(cur, user: UserRegister) -> Optional[Dict]:
    """Create a new user in the database"""
    hashed_password = hash_password(user.password)
    
    cur.execute(
        """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id, username, email
        """,
        (user.username, user.email, hashed_password)
    )
    
    return cur.fetchone()