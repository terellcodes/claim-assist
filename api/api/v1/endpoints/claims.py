"""
Claim Endpoints

Simple API endpoints for claim submission and evaluation.
"""

from fastapi import APIRouter, HTTPException
from models.schemas.claim import ClaimRequest, ClaimResponse
from services.claim_service import claim_service

router = APIRouter(prefix="/claims", tags=["claims"])


@router.post("/submit", response_model=ClaimResponse)
async def submit_claim(claim_request: ClaimRequest):
    """
    Submit a claim for evaluation against an uploaded policy.
    
    - **policy_id**: ID of the uploaded policy to evaluate against
    - **policy_holder_name**: Name of the policy holder
    - **incident_date**: Date when the incident occurred (YYYY-MM-DD)
    - **incident_time**: Optional time of incident (HH:MM)
    - **location**: Where the incident took place  
    - **description**: Detailed description of what happened
    
    Returns evaluation results and either an email draft or suggestions.
    """
    try:
        # Submit claim for evaluation
        result = await claim_service.submit_claim(claim_request)
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error evaluating claim: {str(e)}"
        )


@router.get("/status/{policy_id}")
async def get_claim_status(policy_id: str):
    """
    Get claim status for a policy (placeholder for future enhancement).
    
    - **policy_id**: Policy ID to check claim status for
    """
    # Simple placeholder - in production would track claim history
    return {
        "policy_id": policy_id,
        "status": "ready",
        "message": "Policy ready for claim submission"
    }