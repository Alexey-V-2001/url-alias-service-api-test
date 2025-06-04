"""Click tracking model for detailed analytics."""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from db.database import Base

class Click(Base):
    """Click model for tracking individual clicks on links."""
    
    __tablename__ = "clicks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    link_id = Column(Integer, ForeignKey("links.id"), nullable=False, index=True)
    clicked_at = Column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(String(500), nullable=True)
    
    # Relationship to Link
    link = relationship("Link", back_populates="clicks")
    
    def __repr__(self):
        return f"<Click(link_id={self.link_id}, clicked_at='{self.clicked_at}')>"
