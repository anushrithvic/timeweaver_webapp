"""
Database seeder script to create the initial admin user.

Epic 7: User Story 7.1 - Authentication System

Run this script to create the first admin user for the system.

Usage:
    python -m app.scripts.create_admin
"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password


async def create_admin_user():
    """Create the initial admin user if it doesn't exist."""
    
    # Admin user details
    admin_username = "admin"
    admin_email = "admin@timeweaver.edu"
    admin_password = "admin123"  # CHANGE THIS IN PRODUCTION!
    admin_full_name = "System Administrator"
    
    async with AsyncSessionLocal() as db:
        # Check if admin already exists
        result = await db.execute(select(User).where(User.username == admin_username))
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print(f"Admin user '{admin_username}' already exists!")
            return
        
        # Create admin user
        admin_user = User(
            username=admin_username,
            email=admin_email,
            hashed_password=hash_password(admin_password),
            full_name=admin_full_name,
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        await db.commit()
        await db.refresh(admin_user)
        
        print("=" * 60)
        print("Admin user created successfully!")
        print("=" * 60)
        print(f"Username: {admin_username}")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")
        print(f"Role: {admin_user.role.value}")
        print("=" * 60)
        print("IMPORTANT: Change the password after first login!")
        print("Use POST /api/v1/users/me/password endpoint")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(create_admin_user())
