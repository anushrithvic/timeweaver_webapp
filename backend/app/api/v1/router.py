"""
API v1 Router Configuration

This module configures the main API router for version 1 of the TimeWeaver API.
It aggregates all entity-specific routers and provides a unified entry point
for all API endpoints.

Epic 1: All 6 user stories (1.1-1.6) are represented through the included routers.

Route Structure:
    /api/v1/semesters       - Semester management
    /api/v1/departments     - Department management
    /api/v1/sections        - Section management
    /api/v1/courses         - Course management
    /api/v1/elective-groups - Elective group management
    /api/v1/rooms           - Room/facility management
    /api/v1/time-slots      - Time slot configuration
    /api/v1/constraints     - Constraint rules (+ AI explainability)

All routes are automatically documented in Swagger UI (/docs) and organized
by tags for easy navigation.
"""

from fastapi import APIRouter

# Import all entity-specific endpoint routers
from app.api.v1.endpoints import (
    semesters, departments, sections, courses,
    elective_groups, rooms, time_slots, constraints, auth, users, audit_logs
)

# Create main API router for version 1
api_router = APIRouter()

# Epic 7: Authentication (4 endpoints)
api_router.include_router(auth.router, tags=["authentication"])

# Epic 7: User Management (8 endpoints)
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Epic 7: Audit Logs (2 endpoints - Phase 2)
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["audit-logs"])

# Include all entity routers with their respective prefixes and tags
# Tags are used for grouping in the auto-generated API documentation

# Epic 1: User Story 1.3 - Semesters and Departments
api_router.include_router(semesters.router, prefix="/semesters", tags=["semesters"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])

# Epic 1: User Story 1.3 - Sections
api_router.include_router(sections.router, prefix="/sections", tags=["sections"])

# Epic 1: User Story 1.4 - Courses
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])

# Epic 1: User Story 1.5 - Elective Groups
api_router.include_router(elective_groups.router, prefix="/elective-groups", tags=["elective-groups"])

# Epic 1: User Story 1.6 - Rooms
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])

# Epic 1: User Story 1.1 - Time Slots
api_router.include_router(time_slots.router, prefix="/time-slots", tags=["time-slots"])

# Epic 1: User Story 1.2 - Constraints (includes AI explainability)
api_router.include_router(constraints.router, prefix="/constraints", tags=["constraints"])


@api_router.get("/")
async def api_root():
    """
    API v1 root endpoint - Lists all available endpoints.
    
    Returns a summary of all Epic 1 entities and Epic 7 authentication
    available through the API, useful for API discovery and health checking.
    
    Returns:
        dict: API metadata including version, completion status, and endpoint list
    """
    return {
        "message": "TimeWeaver API v1",
        "epic_1_complete": True,  # All 6 Epic 1 user stories implemented
        "epic_7_complete": True,  # Epic 7: Access Control & Management complete
        "endpoints": {
            "authentication": [
                "/auth/login",
                "/auth/logout",
                "/auth/me",
                "/auth/refresh",
                "/auth/forgot-password",
                "/auth/reset-password"
            ],
            "user_management": [
                "/users",           # List/Create users (admin)
                "/users/{id}",      # Get/Update/Delete user (admin)
                "/users/me/profile",  # Get/Update own profile
                "/users/me/password"  # Change own password
            ],
            "audit_logs": [
                "/audit-logs",      # List audit logs with filters (admin)
                "/audit-logs/{id}"  # Get specific audit log (admin)
            ],
            "academic_entities": [
                "/semesters",        # Academic terms
                "/departments",      # Academic departments
                "/sections",         # Class sections
                "/courses",          # Course definitions
                "/elective-groups",  # Elective course groupings
                "/rooms",            # Facilities/classrooms
                "/time-slots",       # Scheduling time blocks
                "/constraints"       # Scheduling rules (+ AI explain)
            ]
        },
        "total_endpoints": 64  # 48 from Epic 1 + 16 from Epic 7 (6 auth + 8 users + 2 audit logs)
    }
