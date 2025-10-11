from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using argon2"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Ensure 'sub' is a string (JWT standard requires it)
    if 'sub' in to_encode and not isinstance(to_encode['sub'], str):
        to_encode['sub'] = str(to_encode['sub'])
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode JWT token"""
    try:
        print(f"[TOKEN DEBUG] Attempting to verify token...")
        print(f"[TOKEN DEBUG] Token length: {len(token)}")
        print(f"[TOKEN DEBUG] Secret key exists: {bool(settings.SECRET_KEY)}")
        print(f"[TOKEN DEBUG] Algorithm: {settings.ALGORITHM}")
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"[TOKEN DEBUG] Token decoded successfully: {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        print("[TOKEN ERROR] Token has expired")
        return None
    except jwt.JWTError as e:
        print(f"[TOKEN ERROR] JWT decode error: {str(e)}")
        return None
    except Exception as e:
        print(f"[TOKEN ERROR] Unexpected error: {str(e)}")
        return None