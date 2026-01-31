"""
Pydantic schemas for User model.

Epic 7: User Story 7.1 - Authentication System
Epic 7: User Story 7.2 - Role-Based Authorization
"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """Base User schema with common fields"""
    username: str = Field(..., min_length=3, max_length=50, examples=["john_doe"])
    email: EmailStr = Field(..., examples=["john@university.edu"])
    full_name: str = Field(..., min_length=1, max_length=100, examples=["John Doe"])
    role: UserRole = Field(default=UserRole.STUDENT)
    is_active: bool = Field(default=True)


class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = Field(default=UserRole.STUDENT)
    is_active: bool = Field(default=True)
    faculty_id: Optional[int] = None
    student_id: Optional[int] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength
        
        Requirements:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        # Check for special characters
        special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        if not any(c in special_chars for c in v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:\',."<>?/~`)')
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    faculty_id: Optional[int] = None
    student_id: Optional[int] = None


class UserUpdatePassword(BaseModel):
    """Schema for updating user password"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength
        
        Requirements:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        # Check for special characters
        special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        if not any(c in special_chars for c in v):
            raise ValueError('Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:\',."<>?/~`)')
        return v


class UserResponse(BaseModel):
    """Schema for user response (excludes password)"""
    id: int
    username: str
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    is_superuser: bool
    faculty_id: Optional[int]
    student_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Schema for paginated user list response"""
    total: int
    page: int
    size: int
    data: list[UserResponse]
