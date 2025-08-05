from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "cursorai_db")

# Async client for FastAPI
async_client = AsyncIOMotorClient(MONGO_URI)
async_db = async_client[DATABASE_NAME]

# Sync client for background tasks (if needed)
sync_client = MongoClient(MONGO_URI)
sync_db = sync_client[DATABASE_NAME]

# Collections
users_collection = async_db["users"]
questions_collection = async_db["questions"]
quiz_attempts_collection = async_db["quiz_attempts"]
user_answers_collection = async_db["user_answers"]

# Database connection test
async def test_connection():
    """Test database connection"""
    try:
        await async_client.admin.command('ping')
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

# Close database connections
async def close_connection():
    """Close database connections"""
    async_client.close()
    sync_client.close() 