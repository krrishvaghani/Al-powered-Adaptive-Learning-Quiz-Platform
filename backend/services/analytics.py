from typing import Dict, List, Optional
from datetime import datetime, timedelta
from database.mongo import user_answers_collection, quiz_attempts_collection, questions_collection
from bson import ObjectId
import asyncio

class AnalyticsService:
    def __init__(self):
        pass

    async def get_user_analytics(self, user_id: str) -> Dict:
        """Get comprehensive analytics for a specific user"""
        # Get basic stats
        total_quizzes = await self._get_total_quizzes(user_id)
        total_questions = await self._get_total_questions_answered(user_id)
        average_score = await self._get_average_score(user_id)
        accuracy_rate = await self._get_accuracy_rate(user_id)
        
        # Get topic-wise performance
        topic_performance = await self._get_topic_performance(user_id)
        
        # Get difficulty-wise performance
        difficulty_performance = await self._get_difficulty_performance(user_id)
        
        # Get recent activity
        recent_activity = await self._get_recent_activity(user_id)
        
        # Get improvement trends
        improvement_trends = await self._get_improvement_trends(user_id)
        
        return {
            "total_quizzes": total_quizzes,
            "total_questions_answered": total_questions,
            "average_score": average_score,
            "accuracy_rate": accuracy_rate,
            "topic_performance": topic_performance,
            "difficulty_performance": difficulty_performance,
            "recent_activity": recent_activity,
            "improvement_trends": improvement_trends
        }

    async def get_admin_analytics(self) -> Dict:
        """Get analytics for admin dashboard"""
        # Overall platform stats
        total_users = await self._get_total_users()
        total_questions = await self._get_total_questions()
        total_quiz_attempts = await self._get_total_quiz_attempts()
        
        # Performance metrics
        average_platform_score = await self._get_platform_average_score()
        popular_topics = await self._get_popular_topics()
        
        # Recent activity
        recent_quizzes = await self._get_recent_quizzes()
        active_users = await self._get_active_users()
        
        return {
            "total_users": total_users,
            "total_questions": total_questions,
            "total_quiz_attempts": total_quiz_attempts,
            "average_platform_score": average_platform_score,
            "popular_topics": popular_topics,
            "recent_quizzes": recent_quizzes,
            "active_users": active_users
        }

    async def _get_total_quizzes(self, user_id: str) -> int:
        """Get total number of quizzes taken by user"""
        count = await quiz_attempts_collection.count_documents({"user_id": user_id})
        return count

    async def _get_total_questions_answered(self, user_id: str) -> int:
        """Get total number of questions answered by user"""
        count = await user_answers_collection.count_documents({"user_id": user_id})
        return count

    async def _get_average_score(self, user_id: str) -> float:
        """Get average score for user"""
        pipeline = [
            {"$match": {"user_id": user_id, "score": {"$exists": True}}},
            {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
        ]
        
        cursor = quiz_attempts_collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        
        return result[0]["avg_score"] if result else 0.0

    async def _get_accuracy_rate(self, user_id: str) -> float:
        """Get accuracy rate for user"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": None,
                "total_answers": {"$sum": 1},
                "correct_answers": {"$sum": {"$cond": ["$is_correct", 1, 0]}}
            }}
        ]
        
        cursor = user_answers_collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        
        if not result or result[0]["total_answers"] == 0:
            return 0.0
        
        return result[0]["correct_answers"] / result[0]["total_answers"]

    async def _get_topic_performance(self, user_id: str) -> List[Dict]:
        """Get performance by topic"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$lookup": {
                "from": "questions",
                "localField": "question_id",
                "foreignField": "_id",
                "as": "question"
            }},
            {"$unwind": "$question"},
            {"$group": {
                "_id": "$question.topic",
                "total_questions": {"$sum": 1},
                "correct_answers": {"$sum": {"$cond": ["$is_correct", 1, 0]}},
                "avg_time": {"$avg": "$time_taken"}
            }},
            {"$project": {
                "topic": "$_id",
                "total_questions": 1,
                "correct_answers": 1,
                "accuracy": {"$divide": ["$correct_answers", "$total_questions"]},
                "avg_time": 1
            }}
        ]
        
        cursor = user_answers_collection.aggregate(pipeline)
        return await cursor.to_list(length=None)

    async def _get_difficulty_performance(self, user_id: str) -> List[Dict]:
        """Get performance by difficulty level"""
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$lookup": {
                "from": "questions",
                "localField": "question_id",
                "foreignField": "_id",
                "as": "question"
            }},
            {"$unwind": "$question"},
            {"$group": {
                "_id": "$question.difficulty",
                "total_questions": {"$sum": 1},
                "correct_answers": {"$sum": {"$cond": ["$is_correct", 1, 0]}},
                "avg_time": {"$avg": "$time_taken"}
            }},
            {"$project": {
                "difficulty": "$_id",
                "total_questions": 1,
                "correct_answers": 1,
                "accuracy": {"$divide": ["$correct_answers", "$total_questions"]},
                "avg_time": 1
            }}
        ]
        
        cursor = user_answers_collection.aggregate(pipeline)
        return await cursor.to_list(length=None)

    async def _get_recent_activity(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get recent activity for user"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {"$match": {
                "user_id": user_id,
                "timestamp": {"$gte": start_date}
            }},
            {"$lookup": {
                "from": "questions",
                "localField": "question_id",
                "foreignField": "_id",
                "as": "question"
            }},
            {"$unwind": "$question"},
            {"$sort": {"timestamp": -1}},
            {"$limit": 20},
            {"$project": {
                "question_content": "$question.content",
                "topic": "$question.topic",
                "difficulty": "$question.difficulty",
                "is_correct": 1,
                "time_taken": 1,
                "timestamp": 1
            }}
        ]
        
        cursor = user_answers_collection.aggregate(pipeline)
        return await cursor.to_list(length=20)

    async def _get_improvement_trends(self, user_id: str, days: int = 30) -> Dict:
        """Get improvement trends over time"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {"$match": {
                "user_id": user_id,
                "timestamp": {"$gte": start_date}
            }},
            {"$lookup": {
                "from": "questions",
                "localField": "question_id",
                "foreignField": "_id",
                "as": "question"
            }},
            {"$unwind": "$question"},
            {"$group": {
                "_id": {
                    "date": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                    "topic": "$question.topic"
                },
                "total_questions": {"$sum": 1},
                "correct_answers": {"$sum": {"$cond": ["$is_correct", 1, 0]}},
                "avg_time": {"$avg": "$time_taken"}
            }},
            {"$sort": {"_id.date": 1}}
        ]
        
        cursor = user_answers_collection.aggregate(pipeline)
        trends = await cursor.to_list(length=None)
        
        return {
            "daily_performance": trends,
            "overall_trend": self._calculate_trend(trends)
        }

    def _calculate_trend(self, trends: List[Dict]) -> str:
        """Calculate overall trend (improving, declining, stable)"""
        if len(trends) < 2:
            return "insufficient_data"
        
        # Calculate average accuracy for first and last week
        first_week = trends[:7]
        last_week = trends[-7:]
        
        first_avg = sum(t["correct_answers"] / t["total_questions"] for t in first_week) / len(first_week) if first_week else 0
        last_avg = sum(t["correct_answers"] / t["total_questions"] for t in last_week) / len(last_week) if last_week else 0
        
        if last_avg > first_avg + 0.1:
            return "improving"
        elif last_avg < first_avg - 0.1:
            return "declining"
        else:
            return "stable"

    # Admin analytics methods
    async def _get_total_users(self) -> int:
        """Get total number of users"""
        from database.mongo import users_collection
        return await users_collection.count_documents({})

    async def _get_total_questions(self) -> int:
        """Get total number of questions"""
        return await questions_collection.count_documents({})

    async def _get_total_quiz_attempts(self) -> int:
        """Get total number of quiz attempts"""
        return await quiz_attempts_collection.count_documents({})

    async def _get_platform_average_score(self) -> float:
        """Get average score across all users"""
        pipeline = [
            {"$match": {"score": {"$exists": True}}},
            {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
        ]
        
        cursor = quiz_attempts_collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        
        return result[0]["avg_score"] if result else 0.0

    async def _get_popular_topics(self) -> List[Dict]:
        """Get most popular topics"""
        pipeline = [
            {"$lookup": {
                "from": "questions",
                "localField": "question_id",
                "foreignField": "_id",
                "as": "question"
            }},
            {"$unwind": "$question"},
            {"$group": {
                "_id": "$question.topic",
                "total_attempts": {"$sum": 1},
                "avg_accuracy": {"$avg": {"$cond": ["$is_correct", 1, 0]}}
            }},
            {"$sort": {"total_attempts": -1}},
            {"$limit": 10}
        ]
        
        cursor = user_answers_collection.aggregate(pipeline)
        return await cursor.to_list(length=10)

    async def _get_recent_quizzes(self, limit: int = 10) -> List[Dict]:
        """Get recent quiz attempts"""
        cursor = quiz_attempts_collection.find().sort("started_at", -1).limit(limit)
        return await cursor.to_list(length=limit)

    async def _get_active_users(self, days: int = 7) -> int:
        """Get number of active users in the last N days"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {"$match": {"timestamp": {"$gte": start_date}}},
            {"$group": {"_id": "$user_id"}},
            {"$count": "active_users"}
        ]
        
        cursor = user_answers_collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        
        return result[0]["active_users"] if result else 0

# Global instance
analytics_service = AnalyticsService() 