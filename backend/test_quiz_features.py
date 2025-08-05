#!/usr/bin/env python3
"""
Comprehensive test for quiz features
"""
import httpx
import asyncio
import json

async def comprehensive_quiz_test():
    """Test all quiz features"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Comprehensive Quiz Features Test")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # Test 1: Admin Login
        print("1️⃣ Testing Admin Login...")
        admin_login = await client.post(
            f"{base_url}/auth/login",
            data={
                "username": "admin@quizplatform.com",
                "password": "AdminPass123"
            }
        )
        
        if admin_login.status_code == 200:
            admin_token = admin_login.json()['access_token']
            admin_headers = {"Authorization": f"Bearer {admin_token}"}
            print("✅ Admin login successful!")
        else:
            print("❌ Admin login failed")
            return
        
        # Test 2: Student Login
        print("\n2️⃣ Testing Student Login...")
        student_login = await client.post(
            f"{base_url}/auth/login",
            data={
                "username": "test@example.com",
                "password": "TestPass123"
            }
        )
        
        if student_login.status_code == 200:
            student_token = student_login.json()['access_token']
            student_headers = {"Authorization": f"Bearer {student_token}"}
            print("✅ Student login successful!")
        else:
            print("❌ Student login failed")
            return
        
        # Test 3: Admin creates questions
        print("\n3️⃣ Testing Admin Question Creation...")
        questions_to_create = [
            {
                "title": "What is 2 + 2?",
                "content": "What is the result of adding 2 and 2?",
                "question_type": "multiple_choice",
                "difficulty": "easy",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4",
                "explanation": "2 + 2 = 4",
                "points": 1,
                "tags": ["math", "basic"]
            },
            {
                "title": "Is the Earth round?",
                "content": "True or false: The Earth is approximately spherical in shape.",
                "question_type": "true_false",
                "difficulty": "easy",
                "correct_answer": "true",
                "explanation": "The Earth is approximately spherical, though it's slightly flattened at the poles.",
                "points": 1,
                "tags": ["science", "geography"]
            }
        ]
        
        created_questions = []
        for i, question_data in enumerate(questions_to_create, 1):
            create_response = await client.post(
                f"{base_url}/questions/",
                json=question_data,
                headers=admin_headers
            )
            
            if create_response.status_code == 201:
                result = create_response.json()
                created_questions.append(result['question_id'])
                print(f"✅ Question {i} created: {result['title']}")
            else:
                print(f"❌ Failed to create question {i}: {create_response.text}")
        
        # Test 4: Admin gets questions with answers
        print("\n4️⃣ Testing Admin Question Retrieval...")
        for question_id in created_questions:
            get_response = await client.get(
                f"{base_url}/questions/{question_id}",
                headers=admin_headers
            )
            
            if get_response.status_code == 200:
                question = get_response.json()
                print(f"✅ Admin retrieved question: {question['title']}")
                print(f"   Correct Answer: {question['correct_answer']}")
            else:
                print(f"❌ Failed to get question {question_id}")
        
        # Test 5: Student gets questions without answers
        print("\n5️⃣ Testing Student Question Retrieval...")
        for question_id in created_questions:
            get_response = await client.get(
                f"{base_url}/questions/{question_id}/student",
                headers=student_headers
            )
            
            if get_response.status_code == 200:
                question = get_response.json()
                print(f"✅ Student retrieved question: {question['title']}")
                print(f"   Options: {question.get('options', 'N/A')}")
                # Verify no correct answer is exposed
                if 'correct_answer' not in question:
                    print("   ✅ Correct answer hidden from student")
            else:
                print(f"❌ Failed to get question {question_id} for student")
        
        # Test 6: Test role-based access control
        print("\n6️⃣ Testing Role-Based Access Control...")
        
        # Student tries to access admin endpoint
        student_admin_response = await client.get(
            f"{base_url}/questions/{created_questions[0]}",
            headers=student_headers
        )
        
        if student_admin_response.status_code == 403:
            print("✅ Student correctly blocked from admin endpoint")
        else:
            print("❌ Student should be blocked from admin endpoint")
        
        # Test 7: Get question statistics
        print("\n7️⃣ Testing Question Statistics...")
        stats_response = await client.get(
            f"{base_url}/questions/stats/count",
            headers=admin_headers
        )
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print("✅ Question statistics retrieved:")
            print(f"   Total Questions: {stats['total_questions']}")
            print(f"   By Difficulty: {stats['by_difficulty']}")
        else:
            print(f"❌ Failed to get statistics: {stats_response.text}")
        
        # Test 8: Get all questions with filtering
        print("\n8️⃣ Testing Question Filtering...")
        filter_response = await client.get(
            f"{base_url}/questions/?difficulty=easy&tags=math",
            headers=student_headers
        )
        
        if filter_response.status_code == 200:
            filtered_questions = filter_response.json()
            print(f"✅ Retrieved {len(filtered_questions)} filtered questions")
            for q in filtered_questions:
                print(f"   - {q['title']} ({q['difficulty']})")
        else:
            print(f"❌ Failed to filter questions: {filter_response.text}")
        
        # Test 9: Check JSON storage
        print("\n9️⃣ Checking JSON Storage...")
        try:
            with open("data/questions.json", "r") as f:
                questions = json.load(f)
            print(f"✅ JSON file contains {len(questions)} questions")
            print(f"   File location: data/questions.json")
        except Exception as e:
            print(f"❌ Error reading JSON file: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 All quiz feature tests completed!")
    print("📚 Swagger UI: http://127.0.0.1:8000/docs")
    print("🔐 Admin: admin@quizplatform.com / AdminPass123")
    print("👤 Student: test@example.com / TestPass123")

if __name__ == "__main__":
    asyncio.run(comprehensive_quiz_test()) 