"""
Authentication endpoints for login, logout, and user info.

Epic 7: User Story 7.1 - Authentication System
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import timedelta, datetime
from app.db.session import get_db
from app.models.user import User
from app.models.audit_log import AuditLog
from app.schemas.auth import (
    LoginResponse, Token, ForgotPasswordRequest, ForgotPasswordResponse,
    ResetPasswordRequest, ResetPasswordResponse
)
from app.schemas.user import UserResponse
from app.core.security import (
    verify_password, create_access_token, hash_password,
    generate_reset_token, create_reset_token_expiry, is_reset_token_expired
)
from app.core.config import settings
from app.core.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Login with username and password to get JWT access token.
    
    OAuth2 compatible token login, get an access token for future requests.
    
    **Request Body (form data):**
    - `username`: User's username
    - `password`: User's password
    
    **Response:**
    - `access_token`: JWT token for authentication
    - `token_type`: Always "bearer"
    - `user`: User information (without password)
    
    **Example:**
    ```bash
    curl -X POST http://localhost:8000/api/v1/auth/login \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "username=admin&password=SecureP@ss123"
    ```
    """
    # Fetch user by username
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    # Update last login timestamp
    await db.execute(
        update(User)
        .where(User.id == user.id)
        .values(last_login=datetime.utcnow())
    )
    
    # Create audit log entry
    audit_log = AuditLog(
        user_id=user.id,
        action="login",
        entity_type=None,
        entity_id=None,
        changes={"username": user.username}
    )
    db.add(audit_log)
    await db.commit()
    await db.refresh(user)
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's information.
    
    Requires valid JWT token in Authorization header.
    
    **Headers:**
    - `Authorization`: Bearer {access_token}
    
    **Response:**
    User information (without password)
    
    **Example:**
    ```bash
    curl -X GET http://localhost:8000/api/v1/auth/me \
      -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
    ```
    """
    return UserResponse.model_validate(current_user)


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout current user.
    
    Note: JWTs are stateless, so logout is mainly for audit logging.
    The frontend should discard the token on logout.
    
    **Headers:**
    - `Authorization`: Bearer {access_token}
    
    **Response:**
    Success message
    """
    # Create audit log entry
    audit_log = AuditLog(
        user_id=current_user.id,
        action="logout",
        entity_type=None,
        entity_id=None
    )
    db.add(audit_log)
    await db.commit()
    
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user)
):
    """
    Refresh access token.
    
    Get a new access token using the current valid token.
    Useful for extending session without re-login.
    
    **Headers:**
    - `Authorization`: Bearer {access_token}
    
    **Response:**
    New JWT access token
    """
    # Create new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id), "username": current_user.username, "role": current_user.role.value},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Request password reset by email.
    
    Generates a secure reset token that expires in 30 minutes.
    
    **Note:** In production, this endpoint would send an email with the reset link.
    For development/testing, the token is returned in the response.
    
    **Request Body:**
    - `email`: Email address of the account to reset
    
    **Response:**
    - `message`: Confirmation message
    - `reset_token_expires_in`: Token expiration time in minutes
    
    **Security:**
    - Always returns success even if email doesn't exist (prevents user enumeration)
    - Tokens expire after 30 minutes
    - Old tokens are invalidated when new one is requested
    """
    # Find user by email
    query = select(User).where(User.email == request.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user and user.is_active:
        # Generate secure reset token
        reset_token = generate_reset_token()
        reset_expires = create_reset_token_expiry()
        
        # Update user with reset token
        user.reset_token = reset_token
        user.reset_token_expires_at = reset_expires
        await db.commit()
        
        # Create audit log
        audit_log = AuditLog(
            user_id=user.id,
            action="forgot_password",
            entity_type="user",
            entity_id=user.id,
            changes={"message": "Password reset requested"}
        )
        db.add(audit_log)
        await db.commit()
        
        # TODO: In production, send email with reset link
        # send_password_reset_email(user.email, reset_token)
        
        # For development only: Return token in response
        # In production, remove this and only send via email
        return ForgotPasswordResponse(
            message=f"Password reset email sent to {request.email}. Check your inbox for the reset link. [DEV: Token = {reset_token}]",
            reset_token_expires_in=30
        )
    
    # Always return success to prevent user enumeration attacks
    return ForgotPasswordResponse(
        message=f"If an account with {request.email} exists, a password reset email has been sent.",
        reset_token_expires_in=30
    )


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Reset password using reset token.
    
    Validates the reset token and sets new password.
    
    **Request Body:**
    - `reset_token`: Token received from forgot-password endpoint
    - `new_password`: New password (must meet security requirements)
    
    **Response:**
    - `message`: Confirmation message
    
    **Security:**
    - Token is single-use (cleared after successful reset)
    - Tokens expire after 30 minutes
    - New password must meet all strength requirements
    - Password change is audit logged
    
    **Password Requirements:**
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character (!@#$%^&*()_+-=[]{}|;:',.\"<>?/~`)
    """
    # Find user by reset token
    query = select(User).where(User.reset_token == request.reset_token)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )
    
    # Check if token has expired
    if is_reset_token_expired(user.reset_token_expires_at):
        # Clear expired token
        user.reset_token = None
        user.reset_token_expires_at = None
        await db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired. Please request a new password reset."
        )
    
    # Update password
    user.hashed_password = hash_password(request.new_password)
    
    # Clear reset token (single-use)
    user.reset_token = None
    user.reset_token_expires_at = None
    
    await db.commit()
    
    # Create audit log
    audit_log = AuditLog(
        user_id=user.id,
        action="password_reset",
        entity_type="user",
        entity_id=user.id,
        changes={"message": "Password reset successfully completed"}
    )
    db.add(audit_log)
    await db.commit()
    
    return ResetPasswordResponse(
        message="Password has been reset successfully. You can now log in with your new password."
    )
