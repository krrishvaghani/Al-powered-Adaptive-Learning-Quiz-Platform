from typing import List, Dict, Optional
from database.mongo import user_answers_collection
from bson import ObjectId
import asyncio

class AdaptiveLogic:
    def __init__(self):
        self.difficulty_levels = ["easy", "medium", "hard"]
        self.correct_threshold = 3  # Number of correct answers to increase difficulty
        self.incorrect_threshold = 2  # Number of incorrect answers to decrease difficulty

    async def get_user_performance_history(self, user_id: str, topic: str) -> Dict:
        """Get user's recent performance for a specific topic"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$lookup": {
                "from": "questions",
                "localField": "question_id",
                "foreignField": "_id",
                "as": "question"
            }},
            {"$unwind": "$question"},
            {"$match": {"question.topic": topic}},
            {"$sort": {"timestamp": -1}},
            {"$limit": 10}
        ]
        
        cursor = user_answers_collection.aggregate(pipeline)
        recent_answers = await cursor.to_list(length=10)
        
        if not recent_answers:
            return {"difficulty": "medium", "confidence": 0.5}
        
        correct_count = sum(1 for answer in recent_answers if answer["is_correct"])
        total_count = len(recent_answers)
        accuracy = correct_count / total_count if total_count > 0 else 0.5
        
        # Calculate average difficulty of recent questions
        difficulties = [answer["question"]["difficulty"] for answer in recent_answers]
        avg_difficulty = self._calculate_average_difficulty(difficulties)
        
        return {
            "accuracy": accuracy,
            "recent_difficulty": avg_difficulty,
            "total_answered": total_count,
            "correct_count": correct_count
        }

    def _calculate_average_difficulty(self, difficulties: List[str]) -> str:
        """Calculate average difficulty from a list of difficulty levels"""
        difficulty_scores = {"easy": 1, "medium": 2, "hard": 3}
        if not difficulties:
            return "medium"
        
        total_score = sum(difficulty_scores.get(d, 2) for d in difficulties)
        avg_score = total_score / len(difficulties)
        
        if avg_score < 1.5:
            return "easy"
        elif avg_score < 2.5:
            return "medium"
        else:
            return "hard"

    async def determine_next_difficulty(self, user_id: str, topic: str, current_difficulty: str) -> str:
        """Determine the next difficulty level based on user performance"""
        performance = await self.get_user_performance_history(user_id, topic)
        
        # Get recent answers for the current difficulty
        recent_answers = await self._get_recent_answers_by_difficulty(user_id, topic, current_difficulty)
        
        if len(recent_answers) < 3:
            # Not enough data, maintain current difficulty
            return current_difficulty
        
        # Check for streaks
        consecutive_correct = self._get_consecutive_correct(recent_answers)
        consecutive_incorrect = self._get_consecutive_incorrect(recent_answers)
        
        # Adaptive logic
        if consecutive_correct >= self.correct_threshold:
            return self._increase_difficulty(current_difficulty)
        elif consecutive_incorrect >= self.incorrect_threshold:
            return self._decrease_difficulty(current_difficulty)
        else:
            return current_difficulty

    async def _get_recent_answers_by_difficulty(self, user_id: str, topic: str, difficulty: str) -> List[Dict]:
        """Get recent answers for a specific difficulty level"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$lookup": {
                "from": "questions",
                "localField": "question_id",
                "foreignField": "_id",
                "as": "question"
            }},
            {"$unwind": "$question"},
            {"$match": {
                "question.topic": topic,
                "question.difficulty": difficulty
            }},
            {"$sort": {"timestamp": -1}},
            {"$limit": 5}
        ]
        
        cursor = user_answers_collection.aggregate(pipeline)
        return await cursor.to_list(length=5)

    def _get_consecutive_correct(self, answers: List[Dict]) -> int:
        """Get the number of consecutive correct answers"""
        count = 0
        for answer in reversed(answers):  # Start from most recent
            if answer["is_correct"]:
                count += 1
            else:
                break
        return count

    def _get_consecutive_incorrect(self, answers: List[Dict]) -> int:
        """Get the number of consecutive incorrect answers"""
        count = 0
        for answer in reversed(answers):  # Start from most recent
            if not answer["is_correct"]:
                count += 1
            else:
                break
        return count

    def _increase_difficulty(self, current_difficulty: str) -> str:
        """Increase difficulty level"""
        difficulty_map = {"easy": "medium", "medium": "hard", "hard": "hard"}
        return difficulty_map.get(current_difficulty, "medium")

    def _decrease_difficulty(self, current_difficulty: str) -> str:
        """Decrease difficulty level"""
        difficulty_map = {"easy": "easy", "medium": "easy", "hard": "medium"}
        return difficulty_map.get(current_difficulty, "medium")

    async def get_question_recommendations(self, user_id: str, topic: str, num_questions: int = 10) -> List[str]:
        """Get recommended questions based on user's adaptive profile"""
        performance = await self.get_user_performance_history(user_id, topic)
        recommended_difficulty = await self.determine_next_difficulty(user_id, topic, performance.get("recent_difficulty", "medium"))
        
        # Get questions of the recommended difficulty
        from database.mongo import questions_collection
        cursor = questions_collection.find({
            "topic": topic,
            "difficulty": recommended_difficulty
        }).limit(num_questions)
        
        questions = await cursor.to_list(length=num_questions)
        return [str(q["_id"]) for q in questions]

# Global instance
adaptive_logic = AdaptiveLogic() 