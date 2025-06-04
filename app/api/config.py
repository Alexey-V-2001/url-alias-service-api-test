"""API router configuration."""

from fastapi import APIRouter
from api.endpoints import links, stats, users

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    links.router, 
    prefix="/links", 
    tags=["links"]
)

api_router.include_router(
    stats.router, 
    prefix="/stats", 
    tags=["statistics"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)
