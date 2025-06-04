"""Link management endpoints."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from api.deps import get_current_active_user
from db.database import get_db
from models.user import User
from services.link_service import LinkService
from schemas.link import LinkCreate, LinkResponse, LinkUpdate, PaginatedLinksResponse

router = APIRouter()

@router.post("/", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
def create_link(
    link_data: LinkCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new shortened link."""
    try:
        link = LinkService.create_link(db, link_data, current_user.username)
        return link
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create link: {str(e)}"
        )

@router.get("/", response_model=PaginatedLinksResponse)
def list_links(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List user's links with pagination and filtering."""
    try:
        links, total = LinkService.get_user_links(
            db, current_user.username, page, page_size, active
        )
        
        return PaginatedLinksResponse.from_links(links, total, page, page_size)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve links: {str(e)}"
        )

@router.get("/{short_url}", response_model=LinkResponse)
def get_link(
    short_url: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific link by short URL."""
    link = LinkService.get_link_by_short_url(db, short_url)
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    # Check if user owns this link
    if link.created_by != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this link"
        )
    
    return link

@router.put("/{short_url}", response_model=LinkResponse)
def update_link(
    short_url: str,
    link_update: LinkUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a link's status or expiration."""
    link = LinkService.get_link_by_short_url(db, short_url)
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    # Check if user owns this link
    if link.created_by != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this link"
        )
    
    try:
        updated_link = LinkService.update_link(db, link, link_update)
        return updated_link
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update link: {str(e)}"
        )

@router.delete("/{short_url}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(
    short_url: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a link."""
    link = LinkService.get_link_by_short_url(db, short_url)
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found"
        )
    
    # Check if user owns this link
    if link.created_by != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this link"
        )
    
    try:
        LinkService.delete_link(db, link)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete link: {str(e)}"
        )