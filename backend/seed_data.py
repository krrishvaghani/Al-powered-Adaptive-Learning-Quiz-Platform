#!/usr/bin/env python3
"""
Database seeding script for the Adaptive Quiz Learning Platform.
This script creates sample questions and an admin user for testing.
"""

import asyncio
import os
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from utils.hash import hash_password

# Load environment variables
load_dotenv()

# Database connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["adaptive_quiz_db"]

# Sample questions data
SAMPLE_QUESTIONS = [
    # Mathematics - Easy
    {
        "content": "What is 2 + 2?",
        "option_a": "3",
        "option_b": "4",
        "option_c": "5",
        "option_d": "6",
        "correct_option": "B",
        "difficulty": "easy",
        "topic": "mathematics",
        "explanation": "Basic addition: 2 + 2 = 4"
    },
    {
        "content": "What is 5 × 6?",
        "option_a": "25",
        "option_b": "30",
        "option_c": "35",
        "option_d": "40",
        "correct_option": "B",
        "difficulty": "easy",
        "topic": "mathematics",
        "explanation": "Multiplication: 5 × 6 = 30"
    },
    {
        "content": "What is the square root of 16?",
        "option_a": "2",
        "option_b": "4",
        "option_c": "8",
        "option_d": "16",
        "correct_option": "B",
        "difficulty": "easy",
        "topic": "mathematics",
        "explanation": "√16 = 4 because 4 × 4 = 16"
    },
    
    # Mathematics - Medium
    {
        "content": "Solve for x: 2x + 5 = 13",
        "option_a": "3",
        "option_b": "4",
        "option_c": "5",
        "option_d": "6",
        "correct_option": "B",
        "difficulty": "medium",
        "topic": "mathematics",
        "explanation": "2x + 5 = 13 → 2x = 8 → x = 4"
    },
    {
        "content": "What is the area of a circle with radius 5?",
        "option_a": "25π",
        "option_b": "50π",
        "option_c": "75π",
        "option_d": "100π",
        "correct_option": "A",
        "difficulty": "medium",
        "topic": "mathematics",
        "explanation": "Area = πr² = π(5)² = 25π"
    },
    {
        "content": "What is the slope of the line y = 3x + 2?",
        "option_a": "2",
        "option_b": "3",
        "option_c": "5",
        "option_d": "6",
        "correct_option": "B",
        "difficulty": "medium",
        "topic": "mathematics",
        "explanation": "In y = mx + b, m is the slope, so slope = 3"
    },
    
    # Mathematics - Hard
    {
        "content": "What is the derivative of x³?",
        "option_a": "x²",
        "option_b": "2x²",
        "option_c": "3x²",
        "option_d": "4x²",
        "correct_option": "C",
        "difficulty": "hard",
        "topic": "mathematics",
        "explanation": "d/dx(x³) = 3x² using power rule"
    },
    {
        "content": "What is the integral of 2x?",
        "option_a": "x²",
        "option_b": "x² + C",
        "option_c": "2x²",
        "option_d": "2x² + C",
        "correct_option": "B",
        "difficulty": "hard",
        "topic": "mathematics",
        "explanation": "∫2x dx = x² + C (don't forget the constant of integration)"
    },
    
    # Science - Easy
    {
        "content": "What is the chemical symbol for water?",
        "option_a": "H2O",
        "option_b": "CO2",
        "option_c": "O2",
        "option_d": "N2",
        "correct_option": "A",
        "difficulty": "easy",
        "topic": "science",
        "explanation": "Water is composed of 2 hydrogen atoms and 1 oxygen atom"
    },
    {
        "content": "What planet is closest to the Sun?",
        "option_a": "Venus",
        "option_b": "Mercury",
        "option_c": "Earth",
        "option_d": "Mars",
        "correct_option": "B",
        "difficulty": "easy",
        "topic": "science",
        "explanation": "Mercury is the first planet from the Sun"
    },
    
    # Science - Medium
    {
        "content": "What is the atomic number of carbon?",
        "option_a": "4",
        "option_b": "6",
        "option_c": "8",
        "option_d": "12",
        "correct_option": "B",
        "difficulty": "medium",
        "topic": "science",
        "explanation": "Carbon has 6 protons, giving it atomic number 6"
    },
    {
        "content": "What is the largest organ in the human body?",
        "option_a": "Heart",
        "option_b": "Brain",
        "option_c": "Liver",
        "option_d": "Skin",
        "correct_option": "D",
        "difficulty": "medium",
        "topic": "science",
        "explanation": "The skin is the largest organ, covering the entire body"
    },
    
    # History - Easy
    {
        "content": "In which year did World War II end?",
        "option_a": "1943",
        "option_b": "1944",
        "option_c": "1945",
        "option_d": "1946",
        "correct_option": "C",
        "difficulty": "easy",
        "topic": "history",
        "explanation": "World War II ended in 1945 with the surrender of Germany and Japan"
    },
    {
        "content": "Who was the first President of the United States?",
        "option_a": "John Adams",
        "option_b": "Thomas Jefferson",
        "option_c": "George Washington",
        "option_d": "Benjamin Franklin",
        "correct_option": "C",
        "difficulty": "easy",
        "topic": "history",
        "explanation": "George Washington served as the first President from 1789-1797"
    },
    
    # History - Medium
    {
        "content": "What year did Christopher Columbus reach the Americas?",
        "option_a": "1490",
        "option_b": "1492",
        "option_c": "1495",
        "option_d": "1500",
        "correct_option": "B",
        "difficulty": "medium",
        "topic": "history",
        "explanation": "Columbus reached the Americas in 1492, landing in the Bahamas"
    },
    {
        "content": "Which empire was ruled by the Aztecs?",
        "option_a": "Inca",
        "option_b": "Maya",
        "option_c": "Aztec",
        "option_d": "Olmec",
        "correct_option": "C",
        "difficulty": "medium",
        "topic": "history",
        "explanation": "The Aztecs ruled the Aztec Empire in central Mexico"
    }
]

async def seed_database():
    """Seed the database with sample data"""
    print("Starting database seeding...")
    
    # Create admin user
    admin_user = {
        "name": "Admin User",
        "email": "admin@example.com",
        "password_hash": hash_password("admin123"),
        "role": "admin",
        "created_at": datetime.utcnow()
    }
    
    # Check if admin user already exists
    existing_admin = await db.users.find_one({"email": admin_user["email"]})
    if not existing_admin:
        await db.users.insert_one(admin_user)
        print("✅ Admin user created: admin@example.com / admin123")
    else:
        print("ℹ️  Admin user already exists")
    
    # Insert sample questions
    questions_inserted = 0
    for question in SAMPLE_QUESTIONS:
        # Check if question already exists (by content)
        existing_question = await db.questions.find_one({"content": question["content"]})
        if not existing_question:
            question["created_at"] = datetime.utcnow()
            await db.questions.insert_one(question)
            questions_inserted += 1
    
    print(f"✅ {questions_inserted} new questions inserted")
    print(f"ℹ️  Total questions in database: {await db.questions.count_documents({})}")
    
    # Create indexes for better performance
    await db.users.create_index("email", unique=True)
    await db.questions.create_index("topic")
    await db.questions.create_index("difficulty")
    await db.questions.create_index([("topic", 1), ("difficulty", 1)])
    
    print("✅ Database indexes created")
    print("🎉 Database seeding completed successfully!")

async def main():
    """Main function to run the seeding script"""
    try:
        await seed_database()
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main()) 