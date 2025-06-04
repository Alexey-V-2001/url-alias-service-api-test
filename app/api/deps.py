"""API dependencies."""

from fastapi import Depends
from core.security import get_current_user
from models.user import User

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user dependency."""
    return current_user

