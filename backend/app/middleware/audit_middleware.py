"""
Audit Logging Middleware

Epic 7: Phase 2 - Audit Logging Middleware

Automatically captures and logs all state-changing operations (POST, PUT, DELETE).
Extracts user information, request data, and response status for comprehensive audit trails.
"""

import json
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from app.db.session import get_db
from app.services.audit_service import create_audit_log, sanitize_request_data
from app.core.security import decode_access_token


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that automatically logs all state-changing

 operations.
    
    Captures:
    - HTTP method, path, query parameters
    - User ID from JWT token
    - Request body (sanitized)
    - Response status code
    - IP address and user agent
    - Timestamp
    
    Only logs POST, PUT, PATCH, DELETE methods to reduce noise.
    Skips logging for:
    - /docs, /openapi.json (documentation)
    - /health, /metrics (monitoring endpoints)
    """
    
    # Paths to exclude from audit logging
    EXCLUDED_PATHS = {
        "/docs", "/redoc", "/openapi.json",
        "/health", "/metrics", "/favicon.ico"
    }
    
    # Methods that change state (worth logging)
    STATE_CHANGING_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process each request and log if it's a state-changing operation.
        
        Args:
            request: Incoming HTTP request
            call_next: Next middleware/endpoint in chain
            
        Returns:
            Response from the endpoint
        """
        # Skip non-state-changing methods
        if request.method not in self.STATE_CHANGING_METHODS:
            return await call_next(request)
        
        # Skip excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        # Skip audit log endpoints to prevent recursive logging
        if request.url.path.startswith("/api/v1/audit"):
            return await call_next(request)
        
        # Extract user ID from JWT (if present)
        user_id = await self._extract_user_id(request)
        
        # Extract request body (sanitize sensitive data)
        request_body = await self._extract_request_body(request)
        
        # Extract IP address and user agent
        ip_address = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "Unknown")
        
        # Call the actual endpoint
        response = await call_next(request)
        
        # Only log if operation was successful (2xx or 3xx)
        if 200 <= response.status_code < 400:
            await self._create_audit_log(
                user_id=user_id,
                method=request.method,
                path=request.url.path,
                query_params=dict(request.query_params),
                request_body=request_body,
                status_code=response.status_code,
                ip_address=ip_address,
                user_agent=user_agent
            )
        
        return response
    
    async def _extract_user_id(self, request: Request) -> int | None:
        """Extract user ID from JWT token in Authorization header."""
        try:
            auth_header = request.headers.get("authorization", "")
            if not auth_header.startswith("Bearer "):
                return None
            
            token = auth_header.split(" ")[1]
            payload = decode_access_token(token)
            
            if payload:
                return int(payload.get("sub"))
        except Exception:
            pass
        
        return None
    
    async def _extract_request_body(self, request: Request) -> dict:
        """Extract and sanitize request body."""
        try:
            # Read request body
            body_bytes = await request.body()
            
            # Reset request body for downstream handlers
            # This is necessary because reading body() consumes the stream
            async def receive():
                return {"type": "http.request", "body": body_bytes}
            request._receive = receive
            
            if not body_bytes:
                return {}
            
            # Parse JSON body
            body_dict = json.loads(body_bytes.decode('utf-8'))
            
            # Sanitize sensitive fields
            return sanitize_request_data(body_dict)
            
        except Exception:
            return {}
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Get client IP address, accounting for proxies.
        
        Checks X-Forwarded-For header first (for reverse proxies),
        falls back to direct client address.
        """
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            # Get first IP in chain (actual client)
            return forwarded.split(",")[0].strip()
        
        # Direct connection
        if request.client:
            return request.client.host
        
        return "Unknown"
    
    async def _create_audit_log(
        self,
        user_id: int | None,
        method: str,
        path: str,
        query_params: dict,
        request_body: dict,
        status_code: int,
        ip_address: str,
        user_agent: str
    ):
        """
        Create audit log entry in database.
        
        Maps HTTP operations to audit actions and entity types.
        """
        # Determine action from HTTP method
        action_map = {
            "POST": "create",
            "PUT": "update",
            "PATCH": "update",
            "DELETE": "delete"
        }
        action = action_map.get(method, method.lower())
        
        # Extract entity type from path
        # Example: /api/v1/courses/123 -> entity_type = "course"
        entity_type = self._extract_entity_type(path)
        entity_id = self._extract_entity_id(path)
        
        # Build changes dictionary
        changes = {
            "method": method,
            "path": path,
            "query_params": query_params,
            "request_body": request_body,
            "status_code": status_code
        }
        
        # Create log asynchronously (don't block response)
        try:
            # Get database session
            async for db in get_db():
                await create_audit_log(
                    db=db,
                    user_id=user_id,
                    action=action,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    changes=changes,
                    ip_address=ip_address,
                    user_agent=user_agent
                )
                break  # Only need one iteration
        except Exception as e:
            # Don't fail requests if audit logging fails
            # In production, log this error to monitoring system
            print(f"Audit logging failed: {str(e)}")
    
    def _extract_entity_type(self, path: str) -> str:
        """
        Extract entity type from URL path.
        
        Examples:
            /api/v1/courses -> "course"
            /api/v1/users/123 -> "user"
            /api/v1/auth/login -> "auth"
        """
        parts = path.strip("/").split("/")
        
        # Path format: api/v1/{entity}/{id?}
        if len(parts) >= 3:
            entity = parts[2]
            # Singularize (remove trailing 's')
            if entity.endswith("s") and entity not in ["auth", "constraints"]:
                entity = entity[:-1]
            return entity
        
        return "unknown"
    
    def _extract_entity_id(self, path: str) -> int | None:
        """
        Extract entity ID from URL path.
        
        Examples:
            /api/v1/courses/123 -> 123
            /api/v1/users -> None
        """
        parts = path.strip("/").split("/")
        
        # Path format: api/v1/{entity}/{id?}
        if len(parts) >= 4:
            try:
                return int(parts[3])
            except ValueError:
                pass
        
        return None
