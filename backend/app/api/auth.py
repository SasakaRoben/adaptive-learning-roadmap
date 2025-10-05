from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserRegister, UserResponse, UsernameCheck, EmailCheck
from app.schemas.auth import UserLogin, LoginResponse
from app.crud.user import check_username_exists, check_email_exists, create_user
from app.crud.auth import get_user_by_username, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.core.dependencies import get_current_user
from app.core.database import get_db
from datetime import timedelta
from typing import Dict
import logging
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserRegister):
    """Register a new user"""
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Check if username already exists
            if check_username_exists(cur, user.username):
                raise HTTPException(status_code=400, detail="Username already exists")
            
            # Check if email already exists
            if check_email_exists(cur, user.email):
                raise HTTPException(status_code=400, detail="Email already registered")
            
            # Create new user
            new_user = create_user(cur, user)
            
            return UserResponse(
                id=new_user['id'],
                username=new_user['username'],
                email=new_user['email'],
                message="User registered successfully"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error during registration")  # ✅ this prints full traceback
        raise HTTPException(status_code=500, detail="Registration failed")

@router.get("/check-username/{username}", response_model=UsernameCheck)
async def check_username(username: str):
    """Check if username is available"""
    try:
        with get_db() as conn:
            cur = conn.cursor()
            exists = check_username_exists(cur, username)
            return UsernameCheck(available=not exists)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/check-email/{email}", response_model=EmailCheck)
async def check_email(email: str):
    """Check if email is available"""
    try:
        with get_db() as conn:
            cur = conn.cursor()
            exists = check_email_exists(cur, email)
            return EmailCheck(available=not exists)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=LoginResponse)
async def login_user(credentials: UserLogin):
    """Login a user"""
    try:
        with get_db() as conn:
            cur = conn.cursor()
            
            # Try to find user by username or email
            user = get_user_by_username(cur, credentials.username)
            if not user:
                # Try email if username not found
                user = get_user_by_email(cur, credentials.username)
            
            # Check if user exists
            if not user:
                raise HTTPException(status_code=401, detail="Invalid username or password")
            
            # Verify password
            if not verify_password(credentials.password, user['password_hash']):
                raise HTTPException(status_code=401, detail="Invalid username or password")
            
            return LoginResponse(
                id=user['id'],
                username=user['username'],
                email=user['email'],
                message="Login successful"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")