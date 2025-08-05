#!/usr/bin/env python3
"""
Create admin user for testing
"""
import asyncio
from services.auth_service import AuthService
from schemas.user import UserCreate

async def create_admin():
    """Create an admin user"""
    print("👑 Creating Admin User...")
    print("=" * 40)
    
    try:
        # Create admin user data
        admin_data = UserCreate(
            name="Admin User",
            email="admin@quizplatform.com",
            password="AdminPass123",
            role="admin"
        )
        
        print("✅ Admin user data created")
        print(f"Email: {admin_data.email}")
        print(f"Role: {admin_data.role}")
        
        # Register admin user
        result = await AuthService.register_user(admin_data)
        print("✅ Admin user registered successfully!")
        print(f"User ID: {result['user_id']}")
        
        # Test login
        login_result = await AuthService.login_user(admin_data.email, admin_data.password)
        print("✅ Admin login successful!")
        print(f"Access Token: {login_result.access_token[:50]}...")
        print(f"User: {login_result.user.name} ({login_result.user.email})")
        print(f"Role: {login_result.user.role}")
        
        print("\n🎉 Admin user created and ready for testing!")
        print("📝 Use this token for admin operations:")
        print(f"Bearer {login_result.access_token}")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_admin()) 