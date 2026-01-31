"""
Pydantic schemas for authentication endpoints.

Epic 7: User Story 7.1 - Authentication System
"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from app.schemas.user import UserResponse


class Token(BaseModel):
    """JWT Token response schema"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")


class TokenData(BaseModel):
    """Data extracted from JWT token"""
    user_id: int
    username: str
    role: str


class LoginRequest(BaseModel):
    """Login request schema (form data)"""
    username: str = Field(..., examples=["admin"])
    password: str = Field(..., examples=["SecureP@ss123!"])


class LoginResponse(BaseModel):
    """Login response schema with token and user info"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ForgotPasswordRequest(BaseModel):
    """Request schema for forgot password"""
    email: EmailStr = Field(..., description="Email address of the user requesting password reset")


class ForgotPasswordResponse(BaseModel):
    """Response schema for forgot password"""
    message: str = Field(..., description="Success message")
    reset_token_expires_in: int = Field(..., description="Token expiration time in minutes")


class ResetPasswordRequest(BaseModel):
    """Request schema for resetting password with token"""
    reset_token: str = Field(..., description="Password reset token received via email")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength - same as user schema"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        if not any(c in special_chars for c in v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:\',.\"<>?/~`)')
        return v


class ResetPasswordResponse(BaseModel):
    """Response schema for password reset"""
    message: str = Field(..., description="Success message")
