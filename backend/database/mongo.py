from database.connection import db

# Collections
users_collection = db["users"]
questions_collection = db["questions"]
quiz_attempts_collection = db["quiz_attempts"]
user_answers_collection = db["user_answers"]
