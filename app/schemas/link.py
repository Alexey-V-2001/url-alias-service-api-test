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
        if not v.startswith(('http://', 'https://')):
            v = 'https://' + v
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

class LinkStats(BaseModel):
    """Schema for link statistics."""
    short_url: str
    original_url: str
    click_count: int
    created_at: datetime
    is_active: bool
    last_clicked: Optional[datetime] = None
