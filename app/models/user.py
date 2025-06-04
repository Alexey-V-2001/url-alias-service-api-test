"""User model for authentication."""

from sqlalchemy import Column, String, Boolean
from db.database import Base

class User(Base):
    """User model for authentication."""
    
    __tablename__ = "users"
    
    username = Column(String(50), primary_key=True, index=True)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<User(username='{self.username}', is_active={self.is_active})>"
