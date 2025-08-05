from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import HTTPException, status

from models.question import QuestionInDB
from config.database import questions_collection
from schemas.quiz import QuestionCreate, QuestionUpdate, QuestionOut, QuestionWithAnswer

class QuestionService:
    """Question service for admin operations"""
    
    @staticmethod
    async def create_question(question_data: QuestionCreate) -> Dict[str, Any]:
        """
        Create a new question (admin only)
        
        Args:
            question_data: Question creation data
            
        Returns:
            Dict containing creation result
            
        Raises:
            HTTPException: If creation fails
        """
        # Create question model
        question = QuestionInDB(
            title=question_data.title,
            content=question_data.content,
            question_type=question_data.question_type.value,
            difficulty=question_data.difficulty.value,
            options=question_data.options,
            correct_answer=question_data.correct_answer,
            explanation=question_data.explanation,
            points=question_data.points,
            tags=question_data.tags or []
        )
        
        # Insert into database
        result = await questions_collection.insert_one(question.to_dict())
        
        return {
            "message": "Question created successfully",
            "question_id": str(result["inserted_id"]),
            "title": question_data.title
        }
    
    @staticmethod
    async def get_question_by_id(question_id: str) -> Optional[Dict[str, Any]]:
        """
        Get question by ID
        
        Args:
            question_id: Question ID
            
        Returns:
            Question data if found, None otherwise
        """
        try:
            question_data = await questions_collection.find_one({"_id": question_id})
            if not question_data:
                return None
            
            return question_data
        except Exception:
            return None
    
    @staticmethod
    async def get_all_questions(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all questions with pagination
        
        Args:
            skip: Number of questions to skip
            limit: Maximum number of questions to return
            
        Returns:
            List of questions
        """
        try:
            questions = await questions_collection.find()
            return questions[skip:skip + limit]
        except Exception:
            return []
    
    @staticmethod
    async def update_question(question_id: str, question_update: QuestionUpdate) -> Optional[Dict[str, Any]]:
        """
        Update a question
        
        Args:
            question_id: Question ID
            question_update: Update data
            
        Returns:
            Updated question data if successful, None otherwise
        """
        try:
            # Prepare update data
            update_data = {}
            if question_update.title is not None:
                update_data["title"] = question_update.title
            if question_update.content is not None:
                update_data["content"] = question_update.content
            if question_update.question_type is not None:
                update_data["question_type"] = question_update.question_type.value
            if question_update.difficulty is not None:
                update_data["difficulty"] = question_update.difficulty.value
            if question_update.options is not None:
                update_data["options"] = question_update.options
            if question_update.correct_answer is not None:
                update_data["correct_answer"] = question_update.correct_answer
            if question_update.explanation is not None:
                update_data["explanation"] = question_update.explanation
            if question_update.points is not None:
                update_data["points"] = question_update.points
            if question_update.tags is not None:
                update_data["tags"] = question_update.tags
            
            if not update_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields to update"
                )
            
            # Add timestamp
            update_data["updated_at"] = datetime.utcnow()
            
            # Update question
            result = await questions_collection.update_one(
                {"_id": question_id},
                {"$set": update_data}
            )
            
            if result["modified_count"] == 0:
                return None
            
            # Get updated question data
            updated_question = await questions_collection.find_one({"_id": question_id})
            return updated_question
        except Exception:
            return None
    
    @staticmethod
    async def delete_question(question_id: str) -> bool:
        """
        Delete a question
        
        Args:
            question_id: Question ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = await questions_collection.delete_one({"_id": question_id})
            return result["deleted_count"] > 0
        except Exception:
            return False
    
    @staticmethod
    async def get_questions_by_difficulty(difficulty: str) -> List[Dict[str, Any]]:
        """
        Get questions by difficulty level
        
        Args:
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            List of questions with specified difficulty
        """
        try:
            questions = await questions_collection.find({"difficulty": difficulty})
            return questions
        except Exception:
            return []
    
    @staticmethod
    async def get_questions_by_tags(tags: List[str]) -> List[Dict[str, Any]]:
        """
        Get questions by tags
        
        Args:
            tags: List of tags to filter by
            
        Returns:
            List of questions with specified tags
        """
        try:
            # Find questions that have any of the specified tags
            questions = await questions_collection.find({"tags": {"$in": tags}})
            return questions
        except Exception:
            return []
    
    @staticmethod
    async def get_question_count() -> int:
        """
        Get total number of questions
        
        Returns:
            Total question count
        """
        try:
            questions = await questions_collection.find()
            return len(questions)
        except Exception:
            return 0 