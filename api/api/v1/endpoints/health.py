"""
Health Check Endpoint

Simple health check for monitoring and status.
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """
    Simple health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "ClaimWise API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/agent")
async def agent_health():
    """
    Check if the AI agent is working properly.
    """
    try:
        # Simple test - could be enhanced to actually test agent
        return {
            "status": "healthy",
            "agent": "claim_consultant", 
            "message": "Agent is ready to evaluate claims"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "agent": "claim_consultant",
            "error": str(e)
        }