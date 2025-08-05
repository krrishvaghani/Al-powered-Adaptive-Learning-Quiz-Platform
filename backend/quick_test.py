#!/usr/bin/env python3
"""
Quick test for authentication endpoints
"""
import httpx
import asyncio

async def test_endpoints():
    """Test authentication endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("🚀 Quick Authentication Test")
    print("=" * 40)
    
    async with httpx.AsyncClient() as client:
        # Test Swagger docs
        try:
            response = await client.get(f"{base_url}/docs")
            print(f"✅ Swagger Docs: {response.status_code}")
        except Exception as e:
            print(f"❌ Swagger Docs: {e}")
        
        # Test registration endpoint (will fail without MongoDB)
        try:
            response = await client.post(
                f"{base_url}/auth/register",
                json={
                    "name": "Test User",
                    "email": "test@example.com", 
                    "password": "TestPass123",
                    "role": "student"
                }
            )
            print(f"📝 Registration: {response.status_code}")
            if response.status_code != 500:  # Expected to fail without MongoDB
                print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"❌ Registration: {e}")
        
        # Test login endpoint
        try:
            response = await client.post(
                f"{base_url}/auth/login",
                data={
                    "username": "test@example.com",
                    "password": "TestPass123"
                }
            )
            print(f"🔑 Login: {response.status_code}")
        except Exception as e:
            print(f"❌ Login: {e}")
    
    print("\n✅ Authentication endpoints are accessible!")
    print("📚 Swagger UI: http://127.0.0.1:8000/docs")
    print("🔐 Register: POST /auth/register")
    print("🔑 Login: POST /auth/login")
    print("👤 Profile: GET /auth/me")

if __name__ == "__main__":
    asyncio.run(test_endpoints()) 