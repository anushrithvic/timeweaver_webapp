"""
Audit Log model for tracking all system changes.

Epic 7: User Story 7.3 - Audit Logging

This module defines the AuditLog model which records all create, update, and delete
operations performed by users, providing a complete audit trail for accountability.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from app.db.session import Base


class AuditLog(Base):
    """
    Audit log model for tracking all system changes.
    
    Records all state-changing operations (create, update, delete) performed by users.
    Stores before/after values for full traceability and accountability.
    
    Attributes:
        id (int): Primary key, unique identifier
        user_id (int): Foreign key to users table (who made the change)
        action (str): Action performed (create, update, delete, login)
        entity_type (str): Type of entity modified (course, semester, etc.)
        entity_id (int): ID of the modified entity (nullable for list operations)
        changes (dict): JSONB field with before/after values
        ip_address (str): IP address of the client
        user_agent (str): Browser/client user agent string
        timestamp (datetime): When the action occurred
    
    Changes JSONB Format:
        {
            "before": {"field1": "old_value", "field2": "old_value"},
            "after": {"field1": "new_value", "field2": "new_value"}
        }
    
    Example Actions:
        - "create": User created a new entity
        - "update": User modified an entity
        - "delete": User deleted an entity
        - "login": User logged in
        - "logout": User logged out
        - "approve_leave": Admin approved a leave request
    
    Example Usage:
        log = AuditLog(
            user_id=1,
            action="update",
            entity_type="course",
            entity_id=5,
            changes={
                "before": {"credits": 3},
                "after": {"credits": 4}
            },
            ip_address="192.168.1.100"
        )
    """
    __tablename__ = "audit_logs"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # User and Action
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)  # create, update, delete, login
    
    # Entity Information
    entity_type = Column(String(50), nullable=True, index=True)  # course, semester, constraint, etc.
    entity_id = Column(Integer, nullable=True)  # ID of the entity (nullable for bulk operations)
    
    # Change Details
    changes = Column(JSON, nullable=True)  # Before/after values as JSONB
    
    # Request Context
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<AuditLog(id={self.id}, user={self.user_id}, action='{self.action}', entity='{self.entity_type}')>"
