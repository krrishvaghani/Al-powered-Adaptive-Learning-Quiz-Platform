from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

router = APIRouter()

@router.get("/")
async def get_questions():
    """Get all questions"""
    return {"message": "Question management endpoints coming soon!"}

@router.post("/")
async def create_question():
    """Create a new question (Admin only)"""
    return {"message": "Question creation endpoint coming soon!"}

