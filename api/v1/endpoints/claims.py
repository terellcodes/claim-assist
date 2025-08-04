"""
Claim Processing Endpoints

Handles claim submission and evaluation operations.
"""

from fastapi import APIRouter, HTTPException
from models.schemas.claim import ClaimRequest, ClaimResponse
from services.claim_service import claim_service

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("/submit", response_model=ClaimResponse)
async def submit_claim(claim_request: ClaimRequest):
    """
    Submit a claim for AI-powered evaluation.
    
    Args:
        claim_request: Claim details including policy ID and incident description
        
    Returns:
        ClaimResponse with evaluation results and recommendations
    """
    try:
        # Process the claim
        result = await claim_service.submit_claim(claim_request)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process claim: {str(e)}")


@router.get("/{claim_id}")
async def get_claim_status(claim_id: str):
    """
    Get claim status and evaluation results.
    
    Args:
        claim_id: Claim identifier
        
    Returns:
        Claim status and evaluation
    """
    # This would typically fetch from a database
    # For now, return a placeholder response
    raise HTTPException(status_code=501, detail="Claim lookup not yet implemented")