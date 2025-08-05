#!/usr/bin/env python3
"""
Test login functionality
"""
import httpx
import asyncio

async def test_login():
    """Test login endpoint"""
    base_url = "http://127.0.0.1:8000"
    
    print("🔑 Testing Login Endpoint")
    print("=" * 40)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{base_url}/auth/login",
                data={
                    "username": "krish3@gmail.com",
                    "password": "JKVaghani@9"
                }
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Login successful!")
                result = response.json()
                print(f"Access Token: {result['access_token'][:50]}...")
                print(f"User: {result['user']['name']} ({result['user']['email']})")
                return result['access_token']
            else:
                print(f"❌ Login failed: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error during login: {e}")
            return None

if __name__ == "__main__":
    asyncio.run(test_login()) 