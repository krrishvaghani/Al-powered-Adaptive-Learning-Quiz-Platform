#!/usr/bin/env python3
"""
Test /me endpoint with JWT token
"""
import httpx
import asyncio

async def test_me_endpoint():
    """Test /me endpoint with token"""
    base_url = "http://127.0.0.1:8000"
    
    # First get a token by logging in
    async with httpx.AsyncClient() as client:
        # Login to get token
        login_response = await client.post(
            f"{base_url}/auth/login",
            data={
                "username": "krish3@gmail.com",
                "password": "JKVaghani@9"
            }
        )
        
        if login_response.status_code != 200:
            print("❌ Login failed, cannot test /me endpoint")
            return
        
        token = login_response.json()['access_token']
        print(f"✅ Got token: {token[:50]}...")
        
        # Test /me endpoint
        headers = {"Authorization": f"Bearer {token}"}
        me_response = await client.get(
            f"{base_url}/auth/me",
            headers=headers
        )
        
        print(f"\n👤 Testing /me Endpoint")
        print("=" * 40)
        print(f"Status Code: {me_response.status_code}")
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            print("✅ /me endpoint successful!")
            print(f"User ID: {user_data['id']}")
            print(f"Name: {user_data['name']}")
            print(f"Email: {user_data['email']}")
            print(f"Role: {user_data['role']}")
            print(f"Created: {user_data['created_at']}")
        else:
            print(f"❌ /me endpoint failed: {me_response.text}")

if __name__ == "__main__":
    asyncio.run(test_me_endpoint()) 