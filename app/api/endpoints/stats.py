"""Statistics endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_current_active_user
from db.database import get_db
from models.user import User
from services.link_service import LinkService
from schemas.link import LinkStats

router = APIRouter()

@router.get("/", response_model=List[LinkStats])
def get_all_stats(
    db: Session = Depends(get_db)
):
    """Get click statistics for all links, ordered by popularity."""
    try:
        links = LinkService.get_all_links_stats(db)
        
        return [LinkStats.model_validate(link) for link in links]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )

@router.get("/{short_url}", response_model=LinkStats)
def get_link_stats(
    short_url: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get statistics for a specific link."""
    link = LinkService.get_link_stats(db, short_url)
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    try:
        return LinkStats.model_validate(link)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve link statistics: {str(e)}"
        )