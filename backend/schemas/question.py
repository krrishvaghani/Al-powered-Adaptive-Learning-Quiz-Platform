from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionCreate(BaseModel):
    content: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str
    difficulty: DifficultyLevel
    topic: str
    explanation: Optional[str] = None

class QuestionOut(BaseModel):
    id: str
    content: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: DifficultyLevel
    topic: str
    explanation: Optional[str] = None

class QuestionResponse(BaseModel):
    id: str
    content: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: DifficultyLevel
    topic: str

class QuizSubmission(BaseModel):
    quiz_id: str
    answers: List[str]  # user answers

class QuizResult(BaseModel):
    score: int
    total: int
    correct_answers: List[str]
    submitted_answers: List[str]
    accuracy: float
    time_taken: Optional[int] = None
