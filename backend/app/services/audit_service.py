"""
Audit Service

Epic 7: Phase 2 - Audit Logging Middleware

Centralized service for creating and querying audit logs.
Provides utilities for logging actions across the application.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.audit_log import AuditLog
from app.models.user import User


async def create_audit_log(
    db: AsyncSession,
    user_id: Optional[int],
    action: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    changes: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> AuditLog:
    """
    Create an audit log entry.
    
    Args:
        db: Database session
        user_id: ID of user performing the action (None for system actions)
        action: Action performed (create, update, delete, login, etc.)
        entity_type: Type of entity affected (user, semester, course, etc.)
        entity_id: ID of affected entity (if applicable)
        changes: Dictionary of changes made (before/after values)
        ip_address: IP address of the request
        user_agent: User agent string from request
        
    Returns:
        Created AuditLog instance
        
    Example:
        log = await create_audit_log(
            db=db,
            user_id=1,
            action="update",
            entity_type="course",
            entity_id=42,
            changes={"before": {"name": "Old"}, "after": {"name": "New"}},
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0..."
        )
    """
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        changes=changes or {},
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.add(audit_log)
    await db.commit()
    await db.refresh(audit_log)
    
    return audit_log


async def log_action(
    db: AsyncSession,
    user_id: Optional[int],
    action: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    message: Optional[str] = None,
    **metadata
) -> AuditLog:
    """
    Convenience function for logging simple actions.
    
    Args:
        db: Database session
        user_id: ID of user performing action
        action: Action performed
        entity_type: Type of entity
        entity_id: ID of entity
        message: Human-readable message
        **metadata: Additional metadata to include in changes
        
    Returns:
        Created AuditLog instance
        
    Example:
        await log_action(
            db, user_id=1, action="login", entity_type="auth",
            message="User logged in successfully", ip="192.168.1.1"
        )
    """
    changes = metadata.copy()
    if message:
        changes["message"] = message
        
    return await create_audit_log(
        db=db,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        changes=changes,
        ip_address=metadata.get("ip_address"),
        user_agent=metadata.get("user_agent")
    )


async def get_audit_logs(
    db: AsyncSession,
    user_id: Optional[int] = None,
    entity_type: Optional[str] = None,
    action: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
) -> tuple[List[AuditLog], int]:
    """
    Query audit logs with filters and pagination.
    
    Args:
        db: Database session
        user_id: Filter by user ID
        entity_type: Filter by entity type
        action: Filter by action
        start_date: Filter logs after this date
        end_date: Filter logs before this date
        skip: Pagination offset
        limit: Maximum results to return
        
    Returns:
        Tuple of (list of audit logs, total count)
        
    Example:
        logs, total = await get_audit_logs(
            db, user_id=1, action="update", limit=50
        )
    """
    # Build query with filters
    query = select(AuditLog)
    conditions = []
    
    if user_id is not None:
        conditions.append(AuditLog.user_id == user_id)
    if entity_type:
        conditions.append(AuditLog.entity_type == entity_type)
    if action:
        conditions.append(AuditLog.action == action)
    if start_date:
        conditions.append(AuditLog.timestamp >= start_date)
    if end_date:
        conditions.append(AuditLog.timestamp <= end_date)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Apply ordering and pagination
    query = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    logs = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).select_from(AuditLog)
    if conditions:
        count_query = count_query.where(and_(*conditions))
    
    count_result = await db.execute(count_query)
    total = count_result.scalar()
    
    return logs, total


def sanitize_request_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove sensitive data from request body before logging.
    
    Removes passwords, tokens, and other sensitive fields.
    
    Args:
        data: Request data dictionary
        
    Returns:
        Sanitized dictionary
        
    Example:
        sanitized = sanitize_request_data({
            "username": "admin",
            "password": "secret123"  # Will be removed
        })
        # Returns: {"username": "admin"}
    """
    sensitive_fields = {
        'password', 'hashed_password', 'new_password', 'current_password',
        'access_token', 'refresh_token', 'token', 'secret', 'api_key',
        'reset_token', 'authorization'
    }
    
    if not isinstance(data, dict):
        return data
    
    sanitized = {}
    for key, value in data.items():
        if key.lower() in sensitive_fields:
            sanitized[key] = "***REDACTED***"
        elif isinstance(value, dict):
            sanitized[key] = sanitize_request_data(value)
        elif isinstance(value, list):
            sanitized[key] = [
                sanitize_request_data(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            sanitized[key] = value
    
    return sanitized
