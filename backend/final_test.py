#!/usr/bin/env python3
"""
Final comprehensive test for JSON-based authentication system
"""
import httpx
import asyncio
import json

async def comprehensive_test():
    """Test all authentication features"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Comprehensive Authentication Test")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        # Test 1: Registration
        print("1️⃣ Testing User Registration...")
        test_user = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123",
            "role": "student"
        }
        
        register_response = await client.post(
            f"{base_url}/auth/register",
            json=test_user
        )
        
        if register_response.status_code == 201:
            print("✅ Registration successful!")
            user_id = register_response.json()["user_id"]
        else:
            print(f"❌ Registration failed: {register_response.text}")
            return
        
        # Test 2: Login
        print("\n2️⃣ Testing User Login...")
        login_response = await client.post(
            f"{base_url}/auth/login",
            data={
                "username": "test@example.com",
                "password": "TestPass123"
            }
        )
        
        if login_response.status_code == 200:
            print("✅ Login successful!")
            token = login_response.json()["access_token"]
            user_data = login_response.json()["user"]
            print(f"   User: {user_data['name']} ({user_data['email']})")
            print(f"   Role: {user_data['role']}")
        else:
            print(f"❌ Login failed: {login_response.text}")
            return
        
        # Test 3: /me endpoint
        print("\n3️⃣ Testing /me Endpoint...")
        headers = {"Authorization": f"Bearer {token}"}
        me_response = await client.get(
            f"{base_url}/auth/me",
            headers=headers
        )
        
        if me_response.status_code == 200:
            print("✅ /me endpoint successful!")
            me_data = me_response.json()
            print(f"   User ID: {me_data['id']}")
            print(f"   Name: {me_data['name']}")
            print(f"   Email: {me_data['email']}")
        else:
            print(f"❌ /me endpoint failed: {me_response.text}")
        
        # Test 4: Swagger docs
        print("\n4️⃣ Testing Swagger Documentation...")
        docs_response = await client.get(f"{base_url}/docs")
        if docs_response.status_code == 200:
            print("✅ Swagger docs accessible!")
        else:
            print("❌ Swagger docs not accessible!")
        
        # Test 5: Check JSON file
        print("\n5️⃣ Checking JSON Storage...")
        try:
            with open("data/users.json", "r") as f:
                users = json.load(f)
            print(f"✅ JSON file contains {len(users)} users")
            print(f"   File location: data/users.json")
        except Exception as e:
            print(f"❌ Error reading JSON file: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("📚 Swagger UI: http://127.0.0.1:8000/docs")
    print("📁 Data stored in: data/users.json")

if __name__ == "__main__":
    asyncio.run(comprehensive_test()) 