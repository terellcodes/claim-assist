"""
Health Check Routes
"""

from fastapi import APIRouter
from utils.constants import ResponseMessage, StatusCode

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health_check():
    """Health check endpoint for API"""
    return {
        "status": ResponseMessage.SUCCESS,
        "code": StatusCode.HTTP_200_OK,
        "message": "ClaimAssist API is healthy"
    }