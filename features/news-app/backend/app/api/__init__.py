"""
API router aggregation.
"""
from fastapi import APIRouter

from app.api.endpoints import auth, articles, health, sources

api_router = APIRouter()

# Health check
api_router.include_router(health.router, tags=["Health"])

# Auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# Article endpoints
api_router.include_router(articles.router, prefix="/articles", tags=["Articles"])

# Source endpoints
api_router.include_router(sources.router, prefix="/sources", tags=["Sources"])
