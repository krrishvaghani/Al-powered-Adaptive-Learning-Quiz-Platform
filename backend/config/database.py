import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# JSON file storage configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
USERS_FILE = os.path.join(DATA_DIR, "users.json")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")
QUIZZES_FILE = os.path.join(DATA_DIR, "quizzes.json")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

class JSONDatabase:
    """Simple JSON-based database for user storage"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the JSON file exists with empty array"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _read_data(self) -> List[Dict]:
        """Read data from JSON file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _serialize_document(self, document: Dict) -> Dict:
        """Convert datetime objects to strings for JSON serialization"""
        serialized = {}
        for key, value in document.items():
            if isinstance(value, datetime):
                serialized[key] = value.isoformat()
            else:
                serialized[key] = value
        return serialized
    
    def _write_data(self, data: List[Dict]):
        """Write data to JSON file"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    async def find_one(self, query: Dict) -> Optional[Dict]:
        """Find one document matching query"""
        data = self._read_data()
        for item in data:
            if all(item.get(k) == v for k, v in query.items()):
                return item
        return None
    
    async def insert_one(self, document: Dict) -> Dict:
        """Insert one document"""
        data = self._read_data()
        
        # Generate ID if not present
        if '_id' not in document:
            document['_id'] = str(len(data) + 1)
        
        # Add timestamp
        if 'created_at' not in document:
            document['created_at'] = datetime.utcnow().isoformat()
        
        # Convert datetime objects to strings for JSON serialization
        document = self._serialize_document(document)
        
        data.append(document)
        self._write_data(data)
        
        return {"inserted_id": document['_id']}
    
    async def update_one(self, query: Dict, update: Dict) -> Dict:
        """Update one document"""
        data = self._read_data()
        modified_count = 0
        
        for i, item in enumerate(data):
            if all(item.get(k) == v for k, v in query.items()):
                # Update the document
                for key, value in update.get('$set', {}).items():
                    item[key] = value
                modified_count = 1
                break
        
        if modified_count > 0:
            self._write_data(data)
        
        return {"modified_count": modified_count}
    
    async def find(self, query: Dict = None) -> List[Dict]:
        """Find documents matching query"""
        data = self._read_data()
        if query is None:
            return data
        
        result = []
        for item in data:
            if all(item.get(k) == v for k, v in query.items()):
                result.append(item)
        return result

# Initialize JSON database
json_db = JSONDatabase(USERS_FILE)

# Collections (using JSON files)
users_collection = json_db
questions_collection = JSONDatabase(QUESTIONS_FILE)
quizzes_collection = JSONDatabase(QUIZZES_FILE)
quiz_attempts_collection = JSONDatabase(os.path.join(DATA_DIR, "quiz_attempts.json"))
user_answers_collection = JSONDatabase(os.path.join(DATA_DIR, "user_answers.json"))

# Database connection test
async def test_connection():
    """Test database connection"""
    try:
        # Test by reading users file
        data = json_db._read_data()
        print("✅ JSON database connection successful")
        print(f"📁 Users file: {USERS_FILE}")
        print(f"👥 Current users: {len(data)}")
        return True
    except Exception as e:
        print(f"❌ JSON database connection failed: {e}")
        return False

# Close database connections (no-op for JSON files)
async def close_connection():
    """Close database connections"""
    print("📁 JSON database connections closed") 