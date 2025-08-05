import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000"

def register_user():
    """Register a new user"""
    url = f"{BASE_URL}/auth/register"
    
    # User data
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role": "student"
    }
    
    try:
        # Make the request
        response = requests.post(url, json=user_data)
        
        # Check if successful
        if response.status_code == 200:
            print("✅ User registered successfully!")
            print("Response:", response.json())
        else:
            print(f"❌ Registration failed with status code: {response.status_code}")
            print("Error:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure it's running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def login_user():
    """Login with the registered user"""
    url = f"{BASE_URL}/auth/login"
    
    # Login data (form data)
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    
    try:
        # Make the request
        response = requests.post(url, data=login_data)
        
        # Check if successful
        if response.status_code == 200:
            print("✅ Login successful!")
            result = response.json()
            print("Access Token:", result.get("access_token", "Not found"))
            print("User Info:", result.get("user", "Not found"))
        else:
            print(f"❌ Login failed with status code: {response.status_code}")
            print("Error:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure it's running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Testing User Registration...")
    print("=" * 50)
    
    # First register a user
    register_user()
    
    print("\n" + "=" * 50)
    print("🔐 Testing User Login...")
    print("=" * 50)
    
    # Then try to login
    login_user() 