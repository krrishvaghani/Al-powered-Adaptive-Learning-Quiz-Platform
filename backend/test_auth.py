#!/usr/bin/env python3
"""
Test script for authentication system
"""
import asyncio
import httpx
import json
from datetime import datetime

# Test configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_USER = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPass123",
    "role": "student"
}

async def test_register():
    """Test user registration"""
    print("🔐 Testing User Registration...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/auth/register",
                json=TEST_USER
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 201:
                print("✅ Registration successful!")
                return True
            else:
                print("❌ Registration failed!")
                return False
                
        except Exception as e:
            print(f"❌ Error during registration: {e}")
            return False

async def test_login():
    """Test user login"""
    print("\n🔑 Testing User Login...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}/auth/login",
                data={
                    "username": TEST_USER["email"],
                    "password": TEST_USER["password"]
                }
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ Login successful!")
                return response.json().get("access_token")
            else:
                print("❌ Login failed!")
                return None
                
        except Exception as e:
            print(f"❌ Error during login: {e}")
            return None

async def test_me_endpoint(token):
    """Test /me endpoint with token"""
    print("\n👤 Testing /me Endpoint...")
    
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(
                f"{BASE_URL}/auth/me",
                headers=headers
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                print("✅ /me endpoint successful!")
                return True
            else:
                print("❌ /me endpoint failed!")
                return False
                
        except Exception as e:
            print(f"❌ Error during /me test: {e}")
            return False

async def test_swagger_docs():
    """Test if Swagger docs are accessible"""
    print("\n📚 Testing Swagger Documentation...")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/docs")
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Swagger docs accessible!")
                return True
            else:
                print("❌ Swagger docs not accessible!")
                return False
                
        except Exception as e:
            print(f"❌ Error accessing Swagger docs: {e}")
            return False

async def main():
    """Run all tests"""
    print("🚀 Starting Authentication System Tests...")
    print(f"Base URL: {BASE_URL}")
    print(f"Test User: {TEST_USER['email']}")
    print("=" * 50)
    
    # Test Swagger docs
    await test_swagger_docs()
    
    # Test registration
    register_success = await test_register()
    
    # Test login
    token = await test_login()
    
    # Test /me endpoint if we have a token
    if token:
        await test_me_endpoint(token)
    
    print("\n" + "=" * 50)
    print("🏁 Test Summary:")
    print(f"Registration: {'✅ PASS' if register_success else '❌ FAIL'}")
    print(f"Login: {'✅ PASS' if token else '❌ FAIL'}")
    print(f"Swagger Docs: {'✅ PASS' if await test_swagger_docs() else '❌ FAIL'}")
    
    if register_success and token:
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the server logs.")

if __name__ == "__main__":
    asyncio.run(main()) 