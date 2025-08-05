from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class QuizStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class QuizCreate(BaseModel):
    title: str
    topic: str
    difficulty: str = "medium"
    num_questions: int = 10

class QuizStart(BaseModel):
    topic: str
    difficulty: str = "medium"
    num_questions: int = 10

class QuizAnswer(BaseModel):
    question_id: str
    selected_option: str
    time_taken: Optional[int] = None

class QuizSubmission(BaseModel):
    question_ids: List[str]
    selected_options: List[str]
    time_taken_per_question: Optional[List[int]] = None

class QuizResult(BaseModel):
    id: str
    user_id: str
    score: int
    correct_count: int
    total_questions: int
    accuracy: float
    time_taken: Optional[int] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    topic: str
    difficulty: str

class QuizProgress(BaseModel):
    quiz_id: str
    current_question: int
    total_questions: int
    answered_questions: List[str]
    score_so_far: int
    time_elapsed: int

class QuizAnalytics(BaseModel):
    total_quizzes: int
    average_score: float
    best_score: int
    total_questions_answered: int
    accuracy_rate: float
    topics_covered: List[str]
    time_spent_studying: int  # in minutes
