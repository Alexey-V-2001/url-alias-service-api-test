"""Link model for URL shortening."""

from sqlalchemy import Column, String, Boolean, DateTime, Integer
from datetime import datetime, timedelta, timezone
from db.database import Base
from core.config import settings

class Link(Base):
    """Link model for storing shortened URLs."""
    
    __tablename__ = "links"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    short_url = Column(String(100), unique=True, index=True, nullable=False)
    original_url = Column(String(2000), nullable=False)  # Increased length for long URLs
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    expires_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc) + timedelta(days=settings.DEFAULT_LINK_EXPIRY_DAYS),
        nullable=False
    )
    click_count = Column(Integer, default=0, nullable=False)
    created_by = Column(String(50), nullable=True)  # Username who created the link
    
    def __repr__(self):
        return f"<Link(short_url='{self.short_url}', original_url='{self.original_url}', clicks={self.click_count})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if the link has expired."""
        return bool(datetime.now(timezone.utc) > self.expires_at)
    
    @property
    def is_accessible(self) -> bool:
        """Check if the link is accessible (active and not expired)."""
        return bool(self.is_active and not self.is_expired)
