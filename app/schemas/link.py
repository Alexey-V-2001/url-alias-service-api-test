"""Link schemas for request/response validation."""

from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List

class LinkBase(BaseModel):
    """Base link schema."""
    original_url: str

class LinkCreate(LinkBase):
    """Schema for creating a link."""
    expires_in_days: Optional[int] = 1
    
    @field_validator('original_url')
    def validate_url(cls, v):
        """Validate URL format."""
        from urllib.parse import urlparse
        
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        
        # Validate URL structure
        parsed = urlparse(v)
        if not parsed.netloc or '.' not in parsed.netloc:
            raise ValueError('URL must contain a valid domain')
        
        return v

class LinkUpdate(BaseModel):
    """Schema for updating a link."""
    is_active: Optional[bool] = None
    expires_in_days: Optional[int] = None

class LinkResponse(LinkBase):
    """Schema for link response."""
    id: int
    short_url: str
    is_active: bool
    created_at: datetime
    expires_at: datetime
    click_count: int
    created_by: Optional[str]
    
    class Config:
        from_attributes = True

class PaginatedLinksResponse(BaseModel):
    """Schema for paginated links response."""
    total: int
    page: int
    page_size: int
    items: List[LinkResponse]
    
    @classmethod
    def from_links(cls, links: List, total: int, page: int, page_size: int):
        """Create response from Link objects."""
        return cls(
            total=total,
            page=page,
            page_size=page_size,
            items=[LinkResponse.model_validate(link) for link in links]
        )

class LinkStats(BaseModel):
    """Schema for link statistics."""
    short_url: str
    original_url: str
    click_count: int
    created_at: datetime
    is_active: bool
    last_clicked: Optional[datetime] = None
    last_hour_clicks: int = 0
    last_day_clicks: int = 0
    last_week_clicks: int = 0
    last_month_clicks: int = 0
    
    class Config:
        from_attributes = True
