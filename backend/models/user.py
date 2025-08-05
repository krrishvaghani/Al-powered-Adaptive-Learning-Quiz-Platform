from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    """User model for MongoDB"""
    id: Optional[str] = Field(None, alias="_id")
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., unique=True)
    password_hash: str = Field(...)
    role: str = Field(default="student")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "role": "student",
                "is_active": True
            }
        }

class UserInDB(UserModel):
    """User model for database operations"""
    id: Optional[str] = Field(None, alias="_id")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON storage"""
        data = self.dict(exclude={"id"})
        if self.id:
            data["_id"] = self.id
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> "UserInDB":
        """Create from dictionary"""
        if "_id" in data:
            data["id"] = str(data["_id"])
        # Convert string datetime back to datetime object if needed
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and isinstance(data["updated_at"], str):
            data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        return cls(**data)
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
