"""
Health check endpoints
"""

from fastapi import APIRouter
from utils.constants import ResponseMessage, StatusCode

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    """Health check endpoint for API v1"""
    return {
        "status": ResponseMessage.SUCCESS,
        "code": StatusCode.HTTP_200_OK,
        "message": "API v1 is healthy"
    }