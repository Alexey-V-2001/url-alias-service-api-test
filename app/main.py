"""Main FastAPI application."""

from fastapi import FastAPI
import uvicorn

from core.config import settings
from db.database import engine, Base
from api.config import api_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.DESCRIPTION,
              version=settings.VERSION)

# Include API router
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "URL Alias Service",
        "description": settings.DESCRIPTION,
        "version": settings.VERSION,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "url-alias-service"}


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.HOST,
                port=settings.PORT,
                reload=True)
