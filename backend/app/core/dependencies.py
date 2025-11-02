from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.core.database import get_db
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Dependency to get current authenticated user from JWT token
    Usage: user = Depends(get_current_user)
    """
    try:
        token = credentials.credentials
        logger.debug(f"Received authentication token for verification")
        
        payload = verify_token(token)
        
        if payload is None:
            logger.warning("Token verification failed - invalid or expired token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        sub = payload.get("sub")
        if sub is None:
            logger.warning("Token payload missing user ID (sub field)")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format - missing user ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Convert to int; JWT 'sub' should be a string, but we accept int as well
        try:
            user_id: int = int(sub)
        except (TypeError, ValueError):
            logger.warning("Token payload has non-numeric user ID (sub field)")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format - bad subject",
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
            logger.warning(f"User not found in database: user_id={user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        logger.debug(f"User authenticated successfully: {user['username']}")
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )