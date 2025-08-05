#!/usr/bin/env python3
"""
Debug test for registration
"""
import asyncio
from services.auth_service import AuthService
from schemas.user import UserCreate

async def debug_register():
    """Debug registration process"""
    print("🔍 Debugging Registration Process")
    print("=" * 40)
    
    try:
        # Test user data
        user_data = UserCreate(
            name="krish",
            email="krish2@gmail.com",
            password="JKVaghani@9",
            role="student"
        )
        
        print("✅ UserCreate object created successfully")
        print(f"User data: {user_data.dict()}")
        
        # Test registration
        result = await AuthService.register_user(user_data)
        print("✅ Registration successful!")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"❌ Error during registration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_register()) 