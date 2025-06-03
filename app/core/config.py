"""Application configuration settings."""

import os

class Settings:
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    TOKEN_EXPIRE_MINUTES: int = int(os.getenv("TOKEN_EXPIRE_MINUTES", "1440"))  # 24 hours
    
    # Application
    PROJECT_NAME: str = "URL Alias Service"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI service for converting long URLs into short ones"
    
    # URL shortening
    SHORT_URL_LENGTH: int = 8
    DEFAULT_LINK_EXPIRY_DAYS: int = 1
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

settings = Settings()
