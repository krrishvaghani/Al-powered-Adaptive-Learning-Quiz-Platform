from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class QuestionModel(BaseModel):
    """Question model for JSON storage"""
    id: Optional[str] = Field(None, alias="_id")
    title: str = Field(..., min_length=5, max_length=500)
    content: str = Field(..., min_length=10, max_length=2000)
    question_type: str = Field(...)
    difficulty: str = Field(...)
    options: Optional[List[str]] = Field(None)
    correct_answer: str = Field(...)
    explanation: Optional[str] = Field(None, max_length=1000)
    points: int = Field(default=1, ge=1, le=10)
    tags: List[str] = Field(default=[])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "What is the capital of France?",
                "content": "Which city serves as the capital of France?",
                "question_type": "multiple_choice",
                "difficulty": "easy",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct_answer": "Paris",
                "explanation": "Paris is the capital and largest city of France.",
                "points": 1,
                "tags": ["geography", "europe"]
            }
        }

class QuestionInDB(QuestionModel):
    """Question model for database operations"""
    id: Optional[str] = Field(None, alias="_id")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON storage"""
        data = self.dict(exclude={"id"})
        if self.id:
            data["_id"] = self.id
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> "QuestionInDB":
        """Create from dictionary"""
        if "_id" in data:
            data["id"] = str(data["_id"])
        # Convert string datetime back to datetime object if needed
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow() 