#!/usr/bin/env python3
"""
Test question creation with admin authentication
"""
import httpx
import asyncio

async def test_question_creation():
    """Test question creation endpoint"""
    base_url = "http://127.0.0.1:8000"
    
    # First login as admin to get token
    async with httpx.AsyncClient() as client:
        # Login to get admin token
        login_response = await client.post(
            f"{base_url}/auth/login",
            data={
                "username": "admin@quizplatform.com",
                "password": "AdminPass123"
            }
        )
        
        if login_response.status_code != 200:
            print("❌ Admin login failed")
            return
        
        token = login_response.json()['access_token']
        print(f"✅ Got admin token: {token[:50]}...")
        
        # Test question creation
        test_question = {
            "title": "What is the capital of France?",
            "content": "Which city serves as the capital and largest city of France?",
            "question_type": "multiple_choice",
            "difficulty": "easy",
            "options": ["London", "Berlin", "Paris", "Madrid"],
            "correct_answer": "Paris",
            "explanation": "Paris is the capital and largest city of France, located in the north-central part of the country.",
            "points": 1,
            "tags": ["geography", "europe", "capitals"]
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        create_response = await client.post(
            f"{base_url}/questions/",
            json=test_question,
            headers=headers
        )
        
        print(f"\n🔍 Testing Question Creation")
        print("=" * 40)
        print(f"Status Code: {create_response.status_code}")
        
        if create_response.status_code == 201:
            result = create_response.json()
            print("✅ Question created successfully!")
            print(f"Question ID: {result['question_id']}")
            print(f"Title: {result['title']}")
            
            # Test getting all questions
            print("\n📋 Testing Get All Questions...")
            get_response = await client.get(
                f"{base_url}/questions/",
                headers=headers
            )
            
            if get_response.status_code == 200:
                questions = get_response.json()
                print(f"✅ Retrieved {len(questions)} questions")
                if questions:
                    first_question = questions[0]
                    print(f"First Question: {first_question['title']}")
                    print(f"Type: {first_question['question_type']}")
                    print(f"Difficulty: {first_question['difficulty']}")
            else:
                print(f"❌ Failed to get questions: {get_response.text}")
        else:
            print(f"❌ Question creation failed: {create_response.text}")

if __name__ == "__main__":
    asyncio.run(test_question_creation()) 