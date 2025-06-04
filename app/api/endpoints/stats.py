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
        enhanced_stats = LinkService.get_all_enhanced_stats(db)
        
        return [LinkStats(**stats) for stats in enhanced_stats]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve statistics: {str(e)}"
        )

@router.get("/{short_url}", response_model=LinkStats)
def get_link_stats(
    short_url: str,
    db: Session = Depends(get_db)
):
    """Get statistics for a specific link."""
    enhanced_stats = LinkService.get_enhanced_link_stats(db, short_url)
    
    if not enhanced_stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    try:
        return LinkStats(**enhanced_stats)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve link statistics: {str(e)}"
        )