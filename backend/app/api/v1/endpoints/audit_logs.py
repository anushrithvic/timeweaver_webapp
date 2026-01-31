"""
Audit Logs API endpoints for querying system activity.

Epic 7: Phase 2 - Audit Logging Middleware

Provides admin-only access to audit logs with comprehensive filtering.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
from app.db.session import get_db
from app.models.user import User
from app.schemas.audit_log import AuditLogResponse, AuditLogListResponse
from app.core.dependencies import get_current_admin
from app.services.audit_service import get_audit_logs


router = APIRouter()


@router.get("/", response_model=AuditLogListResponse)
async def list_audit_logs(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    entity_type: Optional[str] = Query(None, description="Filter by entity type (course, user, semester, etc.)"),
    action: Optional[str] = Query(None, description="Filter by action (create, update, delete, login, etc.)"),
    start_date: Optional[datetime] = Query(None, description="Filter logs after this date (ISO 8601 format)"),
    end_date: Optional[datetime] = Query(None, description="Filter logs before this date (ISO 8601 format)"),
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=1000, description="Page size (max 1000)"),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    List all audit logs with filtering and pagination.
    
    **Epic 7: Phase 2** - Comprehensive audit trail query
    **Permissions:** Admin only
    
    Returns paginated audit logs showing who did what, when, and from where.
    
    **Filters:**
    - `user_id`: Show only actions by specific user
    - `entity_type`: Show only actions on specific entity (e.g., "course", "user")
    - `action`: Show only specific actions (e.g., "create", "update", "delete")
    - `start_date`: Show logs after this timestamp
    - `end_date`: Show logs before this timestamp
    
    **Response includes:**
    - User who performed the action
    - What action was performed (create/update/delete/login)
    - What entity was affected
    - Request details (sanitized)
    - IP address and user agent
    - Timestamp
    
    **Example:**
    ```bash
    # Get all user updates in the last 7 days
    GET /api/v1/audit-logs?action=update&entity_type=user&start_date=2024-01-24T00:00:00Z
    
    # Get all actions by a specific user
    GET /api/v1/audit-logs?user_id=5&limit=50
    
    # Get all deletions
    GET /api/v1/audit-logs?action=delete
    ```
    """
    # Query audit logs with filters
    logs, total = await get_audit_logs(
        db=db,
        user_id=user_id,
        entity_type=entity_type,
        action=action,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    
    # Calculate page number
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return AuditLogListResponse(
        total=total,
        page=page,
        size=len(logs),
        data=[AuditLogResponse.model_validate(log) for log in logs]
    )


@router.get("/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(
    log_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Get a specific audit log entry by ID.
    
    **Epic 7: Phase 2** - Detailed audit log view
    **Permissions:** Admin only
    
    Returns complete details of a single audit log entry.
    
    **Response includes:**
    - Full request/response details
    - Before and after values (for updates)
    - IP address and user agent
    - Exact timestamp
    """
    from sqlalchemy import select
    from app.models.audit_log import AuditLog
    
    query = select(AuditLog).where(AuditLog.id == log_id)
    result = await db.execute(query)
    log = result.scalar_one_or_none()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit log with ID {log_id} not found"
        )
    
    return AuditLogResponse.model_validate(log)
