from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.core.database import get_db
from typing import Dict
import traceback

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Dependency to get current authenticated user from JWT token
    Usage: user = Depends(get_current_user)
    """
    try:
        token = credentials.credentials
        print(f"[AUTH DEBUG] Received token: {token[:20]}...")  # Print first 20 chars
        
        payload = verify_token(token)
        print(f"[AUTH DEBUG] Token payload: {payload}")
        
        if payload is None:
            print("[AUTH ERROR] Token verification failed - payload is None")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id: int = payload.get("sub")
        print(f"[AUTH DEBUG] Extracted user_id (raw): {user_id}")
        
        # Convert string to int if needed
        if isinstance(user_id, str):
            user_id = int(user_id)
            print(f"[AUTH DEBUG] Converted user_id to int: {user_id}")
        
        if user_id is None:
            print("[AUTH ERROR] No 'sub' field in token payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format - missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Fetch user from database
        with get_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, username, email FROM users WHERE id = %s",
                (user_id,)
            )
            user = cur.fetchone()
        
        if user is None:
            print(f"[AUTH ERROR] User not found in database: user_id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        print(f"[AUTH SUCCESS] User authenticated: {user['username']}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[AUTH ERROR] Unexpected error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )