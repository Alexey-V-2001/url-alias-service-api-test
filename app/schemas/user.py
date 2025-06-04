"""User schemas for request/response validation."""

from pydantic import BaseModel

class UserBase(BaseModel):
    """Base user schema."""
    username: str

class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str

class UserResponse(UserBase):
    """Schema for user response."""
    is_active: bool
    
    class Config:
        from_attributes = True
