from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import datetime

from schemas.user import UserCreate, UserLogin, UserOut, UserUpdate, Token, UserProfile
from models.user import UserInDB
from utils.auth import get_password_hash, verify_password, create_access_token, get_current_user, require_role
from config.database import users_collection

router = APIRouter()

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    """
    Register a new user
    
    - **name**: User's full name (2-100 characters)
    - **email**: Valid email address
    - **password**: Strong password (min 8 chars, uppercase, lowercase, digit)
    - **role**: User role (student, teacher, admin)
    """
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create user model
    user_data = UserInDB(
        name=user.name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        role=user.role.value
    )
    
    # Insert into database
    result = await users_collection.insert_one(user_data.to_dict())
    
    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "email": user.email
    }

@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login user and return access token
    
    - **username**: Email address
    - **password**: User password
    """
    # Find user by email
    user_data = await users_collection.find_one({"email": form_data.username})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user_data["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user_data.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user_data["email"], "role": user_data["role"]}
    )
    
    # Create user response
    user_out = UserOut(
        id=str(user_data["_id"]),
        name=user_data["name"],
        email=user_data["email"],
        role=user_data["role"],
        created_at=user_data["created_at"],
        updated_at=user_data.get("updated_at")
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_out
    )

@router.get("/me", response_model=UserOut)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information
    """
    user_data = await users_collection.find_one({"email": current_user["email"]})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserOut(
        id=str(user_data["_id"]),
        name=user_data["name"],
        email=user_data["email"],
        role=user_data["role"],
        created_at=user_data["created_at"],
        updated_at=user_data.get("updated_at")
    )

@router.put("/me", response_model=UserOut)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user information
    """
    user_data = await users_collection.find_one({"email": current_user["email"]})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prepare update data
    update_data = {}
    if user_update.name is not None:
        update_data["name"] = user_update.name
    if user_update.email is not None:
        # Check if new email already exists
        if user_update.email != user_data["email"]:
            existing_user = await users_collection.find_one({"email": user_update.email})
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
        update_data["email"] = user_update.email
    if user_update.role is not None:
        update_data["role"] = user_update.role.value
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    # Add timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Update user
    result = await users_collection.update_one(
        {"_id": user_data["_id"]},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )
    
    # Get updated user data
    updated_user = await users_collection.find_one({"_id": user_data["_id"]})
    
    return UserOut(
        id=str(updated_user["_id"]),
        name=updated_user["name"],
        email=updated_user["email"],
        role=updated_user["role"],
        created_at=updated_user["created_at"],
        updated_at=updated_user.get("updated_at")
    )

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user profile with statistics
    """
    user_data = await users_collection.find_one({"email": current_user["email"]})
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user statistics (simplified for now)
    # TODO: Implement actual statistics calculation
    total_quizzes = 0
    average_score = 0.0
    total_questions_answered = 0
    
    return UserProfile(
        id=str(user_data["_id"]),
        name=user_data["name"],
        email=user_data["email"],
        role=user_data["role"],
        total_quizzes=total_quizzes,
        average_score=average_score,
        total_questions_answered=total_questions_answered,
        created_at=user_data["created_at"],
        updated_at=user_data.get("updated_at")
    )
