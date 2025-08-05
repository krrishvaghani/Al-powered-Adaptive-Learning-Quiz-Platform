from fastapi import Depends, HTTPException, status
from typing import Callable
from utils.auth import get_current_user

def require_role(required_role: str):
    """
    Dependency to require specific role
    
    Args:
        required_role: Required role (admin, student, teacher)
        
    Returns:
        Dependency function that checks user role
    """
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. {required_role.title()} role required."
            )
        return current_user
    return role_checker

def require_admin():
    """Dependency to require admin role"""
    return require_role("admin")

def require_student():
    """Dependency to require student role"""
    return require_role("student")

def require_teacher():
    """Dependency to require teacher role"""
    return require_role("teacher")

def require_admin_or_teacher():
    """
    Dependency to require admin or teacher role
    """
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in ["admin", "teacher"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Admin or teacher role required."
            )
        return current_user
    return role_checker

def require_any_role():
    """
    Dependency to require any authenticated user
    """
    def role_checker(current_user: dict = Depends(get_current_user)):
        return current_user
    return role_checker 