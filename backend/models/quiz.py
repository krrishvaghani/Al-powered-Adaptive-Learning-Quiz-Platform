from datetime import datetime
from typing import List, Optional, Dict, Any
from bson import ObjectId

class QuestionModel:
    def __init__(
        self,
        content: str,
        option_a: str,
        option_b: str,
        option_c: str,
        option_d: str,
        correct_option: str,
        difficulty: str,
        topic: str,
        explanation: Optional[str] = None,
        created_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id
        self.content = content
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.correct_option = correct_option
        self.difficulty = difficulty
        self.topic = topic
        self.explanation = explanation
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "content": self.content,
            "option_a": self.option_a,
            "option_b": self.option_b,
            "option_c": self.option_c,
            "option_d": self.option_d,
            "correct_option": self.correct_option,
            "difficulty": self.difficulty,
            "topic": self.topic,
            "explanation": self.explanation,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=data.get("_id"),
            content=data["content"],
            option_a=data["option_a"],
            option_b=data["option_b"],
            option_c=data["option_c"],
            option_d=data["option_d"],
            correct_option=data["correct_option"],
            difficulty=data["difficulty"],
            topic=data["topic"],
            explanation=data.get("explanation"),
            created_at=data.get("created_at")
        )

    @property
    def id(self):
        return str(self._id) if self._id else None

class QuizAttemptModel:
    def __init__(
        self,
        user_id: str,
        topic: str,
        difficulty: str,
        questions: List[str],
        started_at: Optional[datetime] = None,
        ended_at: Optional[datetime] = None,
        score: Optional[int] = None,
        total_questions: Optional[int] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id
        self.user_id = user_id
        self.topic = topic
        self.difficulty = difficulty
        self.questions = questions
        self.started_at = started_at or datetime.utcnow()
        self.ended_at = ended_at
        self.score = score
        self.total_questions = total_questions or len(questions)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "questions": self.questions,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "score": self.score,
            "total_questions": self.total_questions
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=data.get("_id"),
            user_id=data["user_id"],
            topic=data["topic"],
            difficulty=data["difficulty"],
            questions=data["questions"],
            started_at=data.get("started_at"),
            ended_at=data.get("ended_at"),
            score=data.get("score"),
            total_questions=data.get("total_questions")
        )

    @property
    def id(self):
        return str(self._id) if self._id else None

class UserAnswerModel:
    def __init__(
        self,
        user_id: str,
        quiz_id: str,
        question_id: str,
        selected_option: str,
        is_correct: bool,
        time_taken: Optional[int] = None,
        timestamp: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id
        self.user_id = user_id
        self.quiz_id = quiz_id
        self.question_id = question_id
        self.selected_option = selected_option
        self.is_correct = is_correct
        self.time_taken = time_taken
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "quiz_id": self.quiz_id,
            "question_id": self.question_id,
            "selected_option": self.selected_option,
            "is_correct": self.is_correct,
            "time_taken": self.time_taken,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=data.get("_id"),
            user_id=data["user_id"],
            quiz_id=data["quiz_id"],
            question_id=data["question_id"],
            selected_option=data["selected_option"],
            is_correct=data["is_correct"],
            time_taken=data.get("time_taken"),
            timestamp=data.get("timestamp")
        )

    @property
    def id(self):
        return str(self._id) if self._id else None
