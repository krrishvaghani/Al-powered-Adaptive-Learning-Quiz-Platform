from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

router = APIRouter()

@router.get("/")
async def get_users():
    """Get all users (Admin only)"""
    return {"message": "User management endpoints coming soon!"}

@router.get("/profile")
async def get_user_profile():
    """Get user profile"""
    return {"message": "User profile endpoint coming soon!"}