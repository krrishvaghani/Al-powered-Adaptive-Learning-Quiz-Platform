from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionCreate(BaseModel):
    """Schema for creating a new question"""
    title: str = Field(..., min_length=5, max_length=500, description="Question title")
    content: str = Field(..., min_length=10, max_length=2000, description="Question content")
    question_type: QuestionType = Field(..., description="Type of question")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level")
    options: Optional[List[str]] = Field(None, description="Multiple choice options")
    correct_answer: str = Field(..., description="Correct answer")
    explanation: Optional[str] = Field(None, max_length=1000, description="Explanation for the answer")
    points: int = Field(default=1, ge=1, le=10, description="Points for this question")
    tags: Optional[List[str]] = Field(default=[], description="Tags for categorization")
    
    @validator('options')
    def validate_options(cls, v, values):
        if values.get('question_type') == QuestionType.MULTIPLE_CHOICE:
            if not v or len(v) < 2:
                raise ValueError('Multiple choice questions must have at least 2 options')
            if len(v) > 6:
                raise ValueError('Multiple choice questions cannot have more than 6 options')
        return v
    
    @validator('correct_answer')
    def validate_correct_answer(cls, v, values):
        if values.get('question_type') == QuestionType.MULTIPLE_CHOICE:
            if values.get('options') and v not in values.get('options', []):
                raise ValueError('Correct answer must be one of the provided options')
        return v

class QuestionUpdate(BaseModel):
    """Schema for updating a question"""
    title: Optional[str] = Field(None, min_length=5, max_length=500)
    content: Optional[str] = Field(None, min_length=10, max_length=2000)
    question_type: Optional[QuestionType] = None
    difficulty: Optional[DifficultyLevel] = None
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = Field(None, max_length=1000)
    points: Optional[int] = Field(None, ge=1, le=10)
    tags: Optional[List[str]] = None

class QuestionOut(BaseModel):
    """Schema for question response (without correct answer)"""
    id: str = Field(..., description="Question ID")
    title: str = Field(..., description="Question title")
    content: str = Field(..., description="Question content")
    question_type: QuestionType = Field(..., description="Type of question")
    difficulty: DifficultyLevel = Field(..., description="Difficulty level")
    options: Optional[List[str]] = Field(None, description="Multiple choice options")
    points: int = Field(..., description="Points for this question")
    tags: List[str] = Field(default=[], description="Tags for categorization")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        from_attributes = True

class QuestionWithAnswer(QuestionOut):
    """Schema for question with correct answer (admin only)"""
    correct_answer: str = Field(..., description="Correct answer")
    explanation: Optional[str] = Field(None, description="Explanation for the answer")

class QuizCreate(BaseModel):
    """Schema for creating a new quiz"""
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=1000)
    time_limit_minutes: Optional[int] = Field(None, ge=5, le=180)
    passing_score: int = Field(default=70, ge=0, le=100)
    is_active: bool = Field(default=True)
    tags: Optional[List[str]] = Field(default=[])
    question_ids: Optional[List[str]] = Field(default=[])

class QuizUpdate(BaseModel):
    """Schema for updating a quiz"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    time_limit_minutes: Optional[int] = Field(None, ge=5, le=180)
    passing_score: Optional[int] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None
    tags: Optional[List[str]] = None
    question_ids: Optional[List[str]] = None

class QuizOut(BaseModel):
    """Schema for quiz response"""
    id: str = Field(...)
    title: str
    description: str
    time_limit_minutes: Optional[int]
    passing_score: int
    is_active: bool
    tags: List[str] = Field(default=[])
    question_ids: List[str] = Field(default=[])
    created_at: datetime
    updated_at: Optional[datetime] = None

class QuizAttemptCreate(BaseModel):
    """Schema for submitting quiz answers"""
    answers: Dict[str, str] = Field(..., description="Question ID to answer mapping")
    time_taken_minutes: Optional[int] = Field(None, ge=0, description="Time taken in minutes")

class QuizAttemptOut(BaseModel):
    """Schema for quiz attempt response"""
    id: str = Field(..., description="Attempt ID")
    quiz_id: str = Field(..., description="Quiz ID")
    user_id: str = Field(..., description="User ID")
    score: int = Field(..., description="Score achieved")
    total_points: int = Field(..., description="Total points possible")
    percentage: float = Field(..., description="Score percentage")
    passed: bool = Field(..., description="Whether quiz was passed")
    time_taken_minutes: Optional[int] = Field(None, description="Time taken in minutes")
    answers: Dict[str, str] = Field(..., description="Submitted answers")
    correct_answers: Dict[str, str] = Field(..., description="Correct answers")
    created_at: datetime = Field(..., description="Attempt timestamp")
    
    class Config:
        from_attributes = True

class UserQuizStats(BaseModel):
    """Schema for user quiz statistics"""
    total_quizzes_taken: int = Field(..., description="Total number of quizzes taken")
    total_questions_answered: int = Field(..., description="Total questions answered")
    average_score: float = Field(..., description="Average score percentage")
    highest_score: float = Field(..., description="Highest score achieved")
    quizzes_passed: int = Field(..., description="Number of quizzes passed")
    total_points_earned: int = Field(..., description="Total points earned")
    favorite_tags: List[str] = Field(default=[], description="Most attempted quiz tags")

class AddQuestionToQuiz(BaseModel):
    question_id: str

class RemoveQuestionFromQuiz(BaseModel):
    question_id: str
