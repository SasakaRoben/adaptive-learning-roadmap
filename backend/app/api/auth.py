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

router = APIRouter(
    prefix="/api",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserResponse, summary="Register new user")
async def register_user(user: UserRegister):
    """
    Register a new user account.
    
    - **username**: Must be 3-50 characters, alphanumeric and underscores only
    - **email**: Valid email address
    - **password**: Minimum 8 characters, must contain uppercase, lowercase, and number
    
    Returns user information and success message.
    """
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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@router.get("/check-username/{username}", response_model=UsernameCheck, summary="Check username availability")
async def check_username(username: str):
    """
    Check if a username is available for registration.
    
    - **username**: Username to check
    
    Returns whether the username is available.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            exists = check_username_exists(cur, username)
            return UsernameCheck(available=not exists)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/check-email/{email}", response_model=EmailCheck, summary="Check email availability")
async def check_email(email: str):
    """
    Check if an email is available for registration.
    
    - **email**: Email address to check
    
    Returns whether the email is available.
    """
    try:
        with get_db() as conn:
            cur = conn.cursor()
            exists = check_email_exists(cur, email)
            return EmailCheck(available=not exists)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=LoginResponse, summary="User login")
async def login_user(credentials: UserLogin):
    """
    Authenticate user and return JWT access token.
    
    - **username**: Username or email address
    - **password**: User password
    
    Returns JWT token for authenticated requests.
    Token expires after 30 minutes.
    """
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
            
            # Create access token
            access_token = create_access_token(
                data={"sub": str(user['id']), "username": user['username']}  # Convert user_id to string
            )
            
            return LoginResponse(
                access_token=access_token,
                token_type="bearer",
                user={
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email']
                }
            )
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/me", summary="Get current user", response_description="Current authenticated user information")
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Requires valid JWT token in Authorization header.
    
    Returns user profile data for the authenticated user.
    """
    return {
        "id": current_user['id'],
        "username": current_user['username'],
        "email": current_user['email']
    }