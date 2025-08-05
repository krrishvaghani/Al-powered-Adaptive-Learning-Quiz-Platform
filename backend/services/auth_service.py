from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from bson import ObjectId

from models.user import UserInDB
from utils.auth import get_password_hash, verify_password, create_access_token
from config.database import users_collection
from schemas.user import UserCreate, UserOut, Token

class AuthService:
    """Authentication service for user management"""
    
    @staticmethod
    async def register_user(user_data: UserCreate) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            user_data: User creation data
            
        Returns:
            Dict containing registration result
            
        Raises:
            HTTPException: If user already exists
        """
        # JSON database is always available
        pass
        
        # Check if user already exists
        existing_user = await users_collection.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create user model
        user = UserInDB(
            name=user_data.name,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            role=user_data.role.value
        )
        
        # Insert into database
        result = await users_collection.insert_one(user.to_dict())
        
        return {
            "message": "User registered successfully",
            "user_id": str(result["inserted_id"]),
            "email": user_data.email
        }
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with email and password
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            User data if authentication successful, None otherwise
        """
        # JSON database is always available
        
        # Find user by email
        user_data = await users_collection.find_one({"email": email})
        if not user_data:
            return None
        
        # Verify password
        if not verify_password(password, user_data["password_hash"]):
            return None
        
        # Check if user is active
        if not user_data.get("is_active", True):
            return None
        
        return user_data
    
    @staticmethod
    async def login_user(email: str, password: str) -> Token:
        """
        Login user and return access token
        
        Args:
            email: User's email
            password: User's password
            
        Returns:
            Token with access token and user info
            
        Raises:
            HTTPException: If authentication fails
        """
        user_data = await AuthService.authenticate_user(email, password)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user_data["email"], "role": user_data["role"]}
        )
        
        # Convert datetime strings to datetime objects if needed
        created_at = user_data["created_at"]
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        updated_at = user_data.get("updated_at")
        if updated_at and isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        
        # Create user response
        user_out = UserOut(
            id=str(user_data["_id"]),
            name=user_data["name"],
            email=user_data["email"],
            role=user_data["role"],
            created_at=created_at,
            updated_at=updated_at
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_out
        )
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email
        
        Args:
            email: User's email
            
        Returns:
            User data if found, None otherwise
        """
        # JSON database is always available
        
        user_data = await users_collection.find_one({"email": email})
        if not user_data:
            return None
        
        return user_data
    
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID
        
        Args:
            user_id: User's ID
            
        Returns:
            User data if found, None otherwise
        """
        try:
            user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
            if not user_data:
                return None
            
            return user_data
        except Exception:
            return None
    
    @staticmethod
    async def update_user_profile(user_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update user profile
        
        Args:
            user_id: User's ID
            update_data: Data to update
            
        Returns:
            Updated user data if successful, None otherwise
        """
        try:
            # Add timestamp
            update_data["updated_at"] = datetime.utcnow()
            
            # Update user
            result = await users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_data}
            )
            
            if result.modified_count == 0:
                return None
            
            # Get updated user data
            updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
            return updated_user
        except Exception:
            return None
    
    @staticmethod
    async def change_password(user_id: str, old_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            user_id: User's ID
            old_password: Current password
            new_password: New password
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get user data
            user_data = await users_collection.find_one({"_id": ObjectId(user_id)})
            if not user_data:
                return False
            
            # Verify old password
            if not verify_password(old_password, user_data["password_hash"]):
                return False
            
            # Hash new password
            new_password_hash = get_password_hash(new_password)
            
            # Update password
            result = await users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "password_hash": new_password_hash,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            return result.modified_count > 0
        except Exception:
            return False 