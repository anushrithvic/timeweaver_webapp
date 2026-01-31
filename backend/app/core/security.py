"""
Security utilities for password hashing and JWT token management.

Epic 7: User Story 7.1 - Authentication System

This module provides:
- Password hashing and verification using bcrypt
- JWT token creation and verification
- Security configuration
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings


# Password hashing context using bcrypt
# truncate_error=False allows passwords longer than 72 bytes (bcrypt's limit)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=False  # Automatically truncate long passwords instead of erroring
)

# JWT Configuration
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.
    
    Bcrypt has a maximum password length of 72 bytes.
    The CryptContext is configured to automatically truncate longer passwords.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
        
    Example:
        hashed = hash_password("MySecureP@ss123")
        # Returns: "$2b$12$KIX..."
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database
        
    Returns:
        True if password matches, False otherwise
        
    Example:
        is_valid = verify_password("MySecureP@ss123", user.hashed_password)
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary of data to encode in the token (usually {"sub": user_id})
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
        
    Example:
        token = create_access_token(
            data={"sub": str(user.id), "role": user.role.value},
            expires_delta=timedelta(minutes=30)
        )
    """
    to_encode = data.copy()
    
    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Encode JWT
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT access token.
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Dictionary with token payload if valid, None otherwise
        
    Example:
        payload = decode_access_token(token)
        if payload:
            user_id = payload.get("sub")
            role = payload.get("role")
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")


def generate_reset_token() -> str:
    """
    Generate a secure random token for password reset.
    
    Creates a URL-safe random token using secrets module.
    Token is 32 bytes (256 bits) which provides strong security.
    
    Returns:
        str: A 43-character URL-safe random string
        
    Example:
        token = generate_reset_token()
        # Returns: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v"
    """
    import secrets
    return secrets.token_urlsafe(32)


def create_reset_token_expiry() -> datetime:
    """
    Create an expiration datetime for password reset token.
    
    Tokens expire 30 minutes after creation for security.
    If a user takes longer than 30 minutes, they must request a new token.
    
    Returns:
        datetime: Expiration timestamp (30 minutes from now)
        
    Example:
        expires = create_reset_token_expiry()
        # Returns: datetime 30 minutes in the future
    """
    return datetime.utcnow() + timedelta(minutes=30)


def is_reset_token_expired(expires_at: Optional[datetime]) -> bool:
    """
    Check if a password reset token has expired.
    
    Args:
        expires_at: The expiration timestamp of the token
        
    Returns:
        bool: True if token is expired or None, False if still valid
        
    Example:
        expired = is_reset_token_expired(user.reset_token_expires_at)
        if expired:
            raise HTTPException(status_code=400, detail="Reset token expired")
    """
    if expires_at is None:
        return True
    return datetime.utcnow() > expires_at


def get_password_hash(password: str) -> str:
    """
    Alias for hash_password for backward compatibility.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
    """
    return hash_password(password)
