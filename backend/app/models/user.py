"""
User model for authentication and authorization.

Epic 7: User Story 7.1 - Authentication System
Epic 7: User Story 7.2 - Role-Based Authorization

This module defines the User model which represents system users with different roles:
- Admin: Full system access
- Faculty: View schedules, set preferences, apply for leave
- Student: View timetables (read-only)
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class UserRole(str, enum.Enum):
    """
    User role enumeration for role-based access control.
    
    Roles:
        ADMIN: Full system access - manage users, all CRUD operations, generate timetables
        FACULTY: View schedules, set time preferences, apply for leave, view workload
        STUDENT: View all timetables and academic data (read-only)
    """
    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"


class User(Base):
    """
    User model for authentication and authorization.
    
    Represents a system user with credentials and role-based permissions.
    Each user has a role that determines what actions they can perform.
    Faculty and Student users can be linked to their respective entities.
    
    Attributes:
        id (int): Primary key, unique identifier
        username (str): Unique username for login
        email (str): Unique email address
        hashed_password (str): Bcrypt hashed password (never store plain text)
        full_name (str): User's full name
        role (UserRole): User's role (admin, faculty, student)
        is_active (bool): Whether the user account is active
        is_superuser (bool): Superuser flag for initial setup
        faculty_id (int): Optional link to Faculty entity (for faculty users)
        student_id (int): Optional link to Student entity (for student users)
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
        last_login (datetime): Last login timestamp
    
    Constraints:
        - Username must be unique
        - Email must be unique
        - Password must be hashed before storage
        - Only faculty users should have faculty_id
        - Only student users should have student_id
    
    Security:
        - Passwords are hashed using bcrypt (via passlib)
        - JWT tokens used for authentication
        - Role-based access control enforced at API level
    
    Example:
        admin = User(
            username="admin",
            email="admin@university.edu",
            hashed_password="$2b$12$...",  # Hashed password
            full_name="System Administrator",
            role=UserRole.ADMIN,
            is_active=True
        )
    """
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication Fields
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    # User Information
    full_name = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT)
    
    # Status Flags
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Links to Faculty/Student entities (Epic 3/4 - nullable for now)
    faculty_id = Column(Integer, nullable=True)  # Will add FK when Faculty model exists
    student_id = Column(Integer, nullable=True)  # Will add FK when Student model exists
    
    # Password Reset Fields
    reset_token = Column(String(255), nullable=True, index=True)
    reset_token_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<User(id={self.id}, username='{self.username}', role='{self.role.value}')>"
