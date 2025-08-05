from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime

from schemas.quiz import QuestionCreate, QuestionUpdate, QuestionOut, QuestionWithAnswer
from services.question_service import QuestionService
from utils.role_auth import require_admin, require_any_role

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_question(
    question: QuestionCreate,
    current_user: dict = Depends(require_admin())
):
    """
    Create a new question (Admin only)
    
    - **title**: Question title (5-500 characters)
    - **content**: Question content (10-2000 characters)
    - **question_type**: Type of question (multiple_choice, true_false, short_answer)
    - **difficulty**: Difficulty level (easy, medium, hard)
    - **options**: Multiple choice options (required for multiple_choice)
    - **correct_answer**: Correct answer
    - **explanation**: Explanation for the answer
    - **points**: Points for this question (1-10)
    - **tags**: Tags for categorization
    """
    return await QuestionService.create_question(question)

@router.get("/", response_model=List[QuestionOut])
async def get_questions(
    skip: int = Query(0, ge=0, description="Number of questions to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of questions to return"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    current_user: dict = Depends(require_any_role())
):
    """
    Get all questions with optional filtering
    
    - **skip**: Number of questions to skip (pagination)
    - **limit**: Maximum number of questions to return
    - **difficulty**: Filter by difficulty level (easy, medium, hard)
    - **tags**: Filter by tags
    """
    questions = await QuestionService.get_all_questions(skip=skip, limit=limit)
    
    # Apply filters
    if difficulty:
        questions = [q for q in questions if q.get("difficulty") == difficulty]
    
    if tags:
        questions = [q for q in questions if any(tag in q.get("tags", []) for tag in tags)]
    
    # Convert to response format (without correct answer for students)
    result = []
    for question in questions:
        # Convert datetime strings to datetime objects if needed
        created_at = question["created_at"]
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        updated_at = question.get("updated_at")
        if updated_at and isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        
        result.append(QuestionOut(
            id=str(question["_id"]),
            title=question["title"],
            content=question["content"],
            question_type=question["question_type"],
            difficulty=question["difficulty"],
            options=question.get("options"),
            points=question["points"],
            tags=question.get("tags", []),
            created_at=created_at,
            updated_at=updated_at
        ))
    
    return result

@router.get("/{question_id}", response_model=QuestionWithAnswer)
async def get_question_with_answer(
    question_id: str,
    current_user: dict = Depends(require_admin())
):
    """
    Get question with correct answer (Admin only)
    """
    question_data = await QuestionService.get_question_by_id(question_id)
    if not question_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Convert datetime strings to datetime objects if needed
    created_at = question_data["created_at"]
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    
    updated_at = question_data.get("updated_at")
    if updated_at and isinstance(updated_at, str):
        updated_at = datetime.fromisoformat(updated_at)
    
    return QuestionWithAnswer(
        id=str(question_data["_id"]),
        title=question_data["title"],
        content=question_data["content"],
        question_type=question_data["question_type"],
        difficulty=question_data["difficulty"],
        options=question_data.get("options"),
        points=question_data["points"],
        tags=question_data.get("tags", []),
        correct_answer=question_data["correct_answer"],
        explanation=question_data.get("explanation"),
        created_at=created_at,
        updated_at=updated_at
    )

@router.get("/{question_id}/student", response_model=QuestionOut)
async def get_question_for_student(
    question_id: str,
    current_user: dict = Depends(require_any_role())
):
    """
    Get question without correct answer (for students)
    """
    question_data = await QuestionService.get_question_by_id(question_id)
    if not question_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Convert datetime strings to datetime objects if needed
    created_at = question_data["created_at"]
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    
    updated_at = question_data.get("updated_at")
    if updated_at and isinstance(updated_at, str):
        updated_at = datetime.fromisoformat(updated_at)
    
    return QuestionOut(
        id=str(question_data["_id"]),
        title=question_data["title"],
        content=question_data["content"],
        question_type=question_data["question_type"],
        difficulty=question_data["difficulty"],
        options=question_data.get("options"),
        points=question_data["points"],
        tags=question_data.get("tags", []),
        created_at=created_at,
        updated_at=updated_at
    )

@router.put("/{question_id}", response_model=QuestionWithAnswer)
async def update_question(
    question_id: str,
    question_update: QuestionUpdate,
    current_user: dict = Depends(require_admin())
):
    """
    Update a question (Admin only)
    """
    updated_question = await QuestionService.update_question(question_id, question_update)
    if not updated_question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found or update failed"
        )
    
    # Convert datetime strings to datetime objects if needed
    created_at = updated_question["created_at"]
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    
    updated_at = updated_question.get("updated_at")
    if updated_at and isinstance(updated_at, str):
        updated_at = datetime.fromisoformat(updated_at)
    
    return QuestionWithAnswer(
        id=str(updated_question["_id"]),
        title=updated_question["title"],
        content=updated_question["content"],
        question_type=updated_question["question_type"],
        difficulty=updated_question["difficulty"],
        options=updated_question.get("options"),
        points=updated_question["points"],
        tags=updated_question.get("tags", []),
        correct_answer=updated_question["correct_answer"],
        explanation=updated_question.get("explanation"),
        created_at=created_at,
        updated_at=updated_at
    )

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: str,
    current_user: dict = Depends(require_admin())
):
    """
    Delete a question (Admin only)
    """
    success = await QuestionService.delete_question(question_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

@router.get("/stats/count", response_model=dict)
async def get_question_stats(
    current_user: dict = Depends(require_admin())
):
    """
    Get question statistics (Admin only)
    """
    total_questions = await QuestionService.get_question_count()
    
    # Get questions by difficulty
    easy_questions = await QuestionService.get_questions_by_difficulty("easy")
    medium_questions = await QuestionService.get_questions_by_difficulty("medium")
    hard_questions = await QuestionService.get_questions_by_difficulty("hard")
    
    return {
        "total_questions": total_questions,
        "by_difficulty": {
            "easy": len(easy_questions),
            "medium": len(medium_questions),
            "hard": len(hard_questions)
        }
    }

