from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegister, UserResponse, UsernameCheck, EmailCheck
from app.crud.user import check_username_exists, check_email_exists, create_user
from app.core.database import get_db

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
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

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