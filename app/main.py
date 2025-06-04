"""Main FastAPI application."""

from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import uvicorn

from core.config import settings
from db.database import get_db, engine, Base
from api.config import api_router
from services.link_service import LinkService

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


@app.get("/{short_url}")
async def redirect_url(short_url: str, request: Request, db: Session = Depends(get_db)):
    """Public endpoint for redirecting shortened URLs."""
    # Get accessible link (active and not expired)
    link = LinkService.get_accessible_link(db, short_url)

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="URL not found, expired, or inactive")

    # Get client information for detailed tracking
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")
    # Increment click count with detailed tracking
    LinkService.increment_click_count(db, link, ip_address=client_ip, user_agent=user_agent)

    # Redirect to original URL
    return RedirectResponse(url=link.original_url,
                            status_code=status.HTTP_301_MOVED_PERMANENTLY)


if __name__ == "__main__":
    uvicorn.run("main:app",
                host=settings.HOST,
                port=settings.PORT,
                reload=True)
