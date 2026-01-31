"""
Authentication and authorization dependencies for FastAPI.

Epic 7: User Story 7.1 - Authentication System
Epic 7: User Story 7.2 - Role-Based Authorization

This module provides dependency functions for:
- Extracting and validating JWT tokens
- Getting the current authenticated user
- Checking user roles and permissions
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.db.session import get_db
from app.models.user import User, UserRole
from app.core.security import decode_access_token


# OAuth2 scheme for token extraction
# tokenUrl points to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.
    
    This dependency:
    1. Extracts the JWT token from the Authorization header
    2. Decodes and validates the token
    3. Fetches the user from the database
    4. Verifies the user is active
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        User object if authentication successful
        
    Raises:
        HTTPException 401: If token is invalid or user not found
        
    Example:
        @router.get("/protected")
        async def protected_route(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello, {current_user.username}"}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extract user ID from token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Fetch user from database
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Alias for get_current_user for backward compatibility.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object if active
    """
    return current_user


def require_role(*required_roles: UserRole):
    """
    Dependency factory for role-based access control.
    
    Creates a dependency that checks if the current user has one of the required roles.
    

    Args:
        *required_roles: One or more UserRole enum values
        
    Returns:
        Dependency function that validates user role
        
    Raises:
        HTTPException 403: If user doesn't have required role
        
    Example:
        # Admin only endpoint
        @router.post("/users", dependencies=[Depends(require_role(UserRole.ADMIN))])
        async def create_user(...):
            pass
        
        # Admin or Faculty endpoint
        @router.get("/schedules", dependencies=[Depends(require_role(UserRole.ADMIN, UserRole.FACULTY))])
        async def get_schedules(...):
            pass
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {[r.value for r in required_roles]}"
            )
        return current_user
    
    return role_checker


async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current user and verify they are an admin.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object if user is admin
        
    Raises:
        HTTPException 403: If user is not an admin
        
    Example:
        @router.delete("/users/{id}")
        async def delete_user(user_id: int, admin: User = Depends(get_current_admin)):
            # Only admins can reach this code
            pass
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def get_current_faculty(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current user and verify they are faculty.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object if user is faculty
        
    Raises:
        HTTPException 403: If user is not faculty
    """
    if current_user.role != UserRole.FACULTY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Faculty access required"
        )
    return current_user


async def get_current_student(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current user and verify they are a student.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object if user is student
        
    Raises:
        HTTPException 403: If user is not a student
        
    Example:
        @router.get("/my-timetable")
        async def get_my_timetable(student: User = Depends(get_current_student)):
            # Only students can reach this code
            pass
    """
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access required"
        )
    return current_user


# Optional user dependency (doesn't raise exception if not authenticated)
async def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    
    Useful for endpoints that change behavior based on authentication
    but don't require it.
    
    Args:
        token: Optional JWT token
        db: Database session
        
    Returns:
        User object if authenticated, None otherwise
    """
    if token is None:
        return None
    
    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None
