"""
JWT Authentication with Stride ID SSO Integration

This module provides JWT token validation middleware that integrates with
the central Stride Ahead SSO service (Stride ID) for authentication.
"""

import os
from typing import Optional
from datetime import datetime, timedelta

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings


# Security scheme for Swagger UI
security = HTTPBearer()


class TokenData(BaseModel):
    """JWT token payload data"""
    user_id: str
    email: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = "user"
    tenant_id: Optional[str] = None


class User(BaseModel):
    """Authenticated user model"""
    id: str
    email: Optional[str]
    name: Optional[str]
    role: str = "user"
    tenant_id: Optional[str] = None


async def validate_stride_id_token(token: str) -> Optional[User]:
    """
    Validate JWT token with Stride ID SSO service
    
    Args:
        token: JWT token string
        
    Returns:
        User object if token is valid, None otherwise
    """
    try:
        # Option 1: Validate with Stride ID service (recommended for production)
        if settings.STRIDE_ID_VALIDATION_URL:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.STRIDE_ID_VALIDATION_URL}/validate",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    user_data = response.json()
                    return User(
                        id=user_data.get("user_id") or user_data.get("id"),
                        email=user_data.get("email"),
                        name=user_data.get("name"),
                        role=user_data.get("role", "user"),
                        tenant_id=user_data.get("tenant_id")
                    )
                return None
        
        # Option 2: Local JWT validation (fallback for development)
        # Decode and verify JWT token locally
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Extract user data from token
        user_id: str = payload.get("sub") or payload.get("user_id")
        if user_id is None:
            return None
            
        return User(
            id=user_id,
            email=payload.get("email"),
            name=payload.get("name"),
            role=payload.get("role", "user"),
            tenant_id=payload.get("tenant_id")
        )
        
    except JWTError:
        return None
    except httpx.RequestError:
        # If Stride ID service is unavailable, fall back to local validation
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get("sub") or payload.get("user_id")
            if user_id:
                return User(
                    id=user_id,
                    email=payload.get("email"),
                    name=payload.get("name"),
                    role=payload.get("role", "user"),
                    tenant_id=payload.get("tenant_id")
                )
        except JWTError:
            pass
        return None
    except Exception as e:
        print(f"Token validation error: {e}")
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Dependency to get the current authenticated user
    
    Usage:
        @router.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"user_id": user.id}
    
    Args:
        credentials: HTTP Bearer token from Authorization header
        
    Returns:
        Authenticated User object
        
    Raises:
        HTTPException: If token is invalid or missing
    """
    token = credentials.credentials
    
    user = await validate_stride_id_token(token)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current active user (can add additional checks here)
    
    Usage:
        @router.get("/protected")
        async def protected_route(user: User = Depends(get_current_active_user)):
            return {"user_id": user.id}
    """
    # Add additional checks here if needed (e.g., user is not disabled)
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current admin user
    
    Usage:
        @router.get("/admin/dashboard")
        async def admin_dashboard(admin: User = Depends(get_current_admin_user)):
            return {"message": "Admin access granted"}
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object if user is admin
        
    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token
    
    Note: In production, tokens should be created by Stride ID service.
    This function is provided for development/testing purposes only.
    
    Args:
        data: Dictionary of claims to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


# Optional endpoints for development/testing
def create_auth_router():
    """
    Create authentication router for development/testing
    
    In production, authentication should be handled by Stride ID service.
    This router is only for local development and testing.
    """
    from fastapi import APIRouter
    
    router = APIRouter(prefix="/auth", tags=["Authentication"])
    
    @router.post("/token")
    async def login_for_testing(user_id: str, email: str = None, name: str = None):
        """
        Development endpoint to generate test JWT tokens
        
        **WARNING: Remove this endpoint in production!**
        """
        if not settings.DEBUG:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Endpoint not available in production"
            )
        
        access_token = create_access_token(
            data={
                "sub": user_id,
                "user_id": user_id,
                "email": email,
                "name": name,
                "role": "user"
            }
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    @router.get("/me")
    async def get_current_user_info(user: User = Depends(get_current_user)):
        """Get current authenticated user information"""
        return user
    
    return router
