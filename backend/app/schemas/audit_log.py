"""
Pydantic schemas for Audit Log model.

Epic 7: User Story 7.3 - Audit Logging
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class AuditLogBase(BaseModel):
    """Base Audit Log schema"""
    action: str = Field(..., examples=["create", "update", "delete", "login"])
    entity_type: Optional[str] = Field(None, examples=["course", "semester", "constraint"])
    entity_id: Optional[int] = None
    changes: Optional[Dict[str, Any]] = None


class AuditLogCreate(AuditLogBase):
    """Schema for creating an audit log entry"""
    user_id: int
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    """Schema for audit log response"""
    id: int
    user_id: int
    ip_address: Optional[str]
    user_agent: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    """Schema for paginated audit log list response"""
    total: int
    page: int
    size: int
    data: list[AuditLogResponse]
