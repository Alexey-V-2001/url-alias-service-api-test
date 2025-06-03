"""Service layer for link operations."""

import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from models.link import Link
from schemas.link import LinkCreate, LinkUpdate
from core.config import settings

class LinkService:
    """Service class for link operations."""
    
    @staticmethod
    def generate_short_url(length: Optional[int] = None) -> str:
        """Generate a random short URL."""
        if length is None:
            length = settings.SHORT_URL_LENGTH
        
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def create_link(db: Session, link_data: LinkCreate, username: str) -> Link:
        """Create a new shortened link."""
        # Generate unique short URL
        short_url = LinkService.generate_short_url()
        
        # Ensure uniqueness
        while db.query(Link).filter(Link.short_url == short_url).first():
            short_url = LinkService.generate_short_url()
        
        # Calculate expiration date
        expires_at = datetime.now(timezone.utc) + timedelta(days=link_data.expires_in_days)
        
        # Create link object
        db_link = Link(
            short_url=short_url,
            original_url=link_data.original_url,
            expires_at=expires_at,
            created_by=username
        )
        
        db.add(db_link)
        db.commit()
        db.refresh(db_link)
        
        return db_link
    
    @staticmethod
    def get_link_by_short_url(db: Session, short_url: str) -> Optional[Link]:
        """Get a link by its short URL."""
        return db.query(Link).filter(Link.short_url == short_url).first()
    
    @staticmethod
    def get_accessible_link(db: Session, short_url: str) -> Optional[Link]:
        """Get an accessible link (active and not expired)."""
        link = db.query(Link).filter(
            and_(
                Link.short_url == short_url,
                Link.is_active == True,
                Link.expires_at > datetime.now(timezone.utc)
            )
        ).first()
        return link
    
    @staticmethod
    def increment_click_count(db: Session, link: Link) -> Link:
        """Increment the click count for a link."""
        link.click_count += 1
        db.commit()
        db.refresh(link)
        return link
    
    @staticmethod
    def get_user_links(
        db: Session, 
        username: str,
        page: int = 1, 
        page_size: int = 10,
        active: Optional[bool] = None
    ) -> tuple[List[Link], int]:
        """Get paginated links for a user with optional filtering."""
        query = db.query(Link).filter(Link.created_by == username)
        
        # Apply active filter if provided
        if active is not None:
            query = query.filter(Link.is_active == active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        links = query.order_by(desc(Link.created_at)).offset((page - 1) * page_size).limit(page_size).all()
        
        return links, total
    
    @staticmethod
    def update_link(db: Session, link: Link, link_update: LinkUpdate) -> Link:
        """Update a link."""
        update_data = link_update.dict(exclude_unset=True)
        
        # Handle expires_in_days conversion
        if 'expires_in_days' in update_data:
            expires_in_days = update_data.pop('expires_in_days')
            update_data['expires_at'] = datetime.now(timezone.utc) + timedelta(days=expires_in_days)
        
        for field, value in update_data.items():
            setattr(link, field, value)
        
        db.commit()
        db.refresh(link)
        
        return link
    
    @staticmethod
    def delete_link(db: Session, link: Link) -> bool:
        """Delete a link."""
        db.delete(link)
        db.commit()
        return True
    
    @staticmethod
    def get_all_links_stats(db: Session) -> List[Link]:
        """Get all links ordered by click count for statistics."""
        return db.query(Link).order_by(desc(Link.click_count)).all()
    
    @staticmethod
    def get_link_stats(db: Session, short_url: str) -> Optional[Link]:
        """Get statistics for a specific link."""
        return db.query(Link).filter(Link.short_url == short_url).first()
