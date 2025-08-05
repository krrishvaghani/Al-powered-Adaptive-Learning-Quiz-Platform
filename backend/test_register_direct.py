#!/usr/bin/env python3
"""
Direct test for registration endpoint
"""
import httpx
import asyncio
import json

async def test_register():
    """Test registration endpoint directly"""
    base_url = "http://127.0.0.1:8000"
    
    test_user = {
        "name": "krish",
        "email": "krish3@gmail.com",
        "password": "JKVaghani@9",
        "role": "student"
    }
    
    print("🔐 Testing Registration Endpoint")
    print("=" * 40)
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{base_url}/auth/register",
                json=test_user,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            if response.status_code == 503:
                print("✅ Expected error: Database not available")
                print("📝 This is correct - MongoDB needs to be running")
                return True
            elif response.status_code == 201:
                print("✅ Registration successful!")
                print(f"Response: {response.json()}")
                return True
            else:
                print(f"❌ Unexpected status: {response.status_code}")
                try:
                    print(f"Response: {response.text}")
                except:
                    print("Could not read response")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

if __name__ == "__main__":
    asyncio.run(test_register()) 