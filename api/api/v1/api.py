"""
API v1 Router

Aggregates all v1 endpoints into a single router.
"""

from fastapi import APIRouter
from .endpoints import policies, claims, health

api_router = APIRouter(prefix="/v1")

# Include all endpoint routers
api_router.include_router(health.router)
api_router.include_router(policies.router)
api_router.include_router(claims.router)