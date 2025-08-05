from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

router = APIRouter()

@router.get("/")
async def get_quizzes():
    """Get available quizzes"""
    return {"message": "Quiz endpoints coming soon!"}

@router.post("/start")
async def start_quiz():
    """Start a new quiz"""
    return {"message": "Quiz start endpoint coming soon!"}

@router.post("/submit")
async def submit_quiz():
    """Submit quiz answers"""
    return {"message": "Quiz submit endpoint coming soon!"}
