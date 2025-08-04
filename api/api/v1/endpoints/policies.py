"""
Policy Endpoints

Simple API endpoints for policy upload and management.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from models.schemas.policy import PolicyUploadResponse
from models.schemas.base import ErrorResponse
from services.policy_service import policy_service

router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("/upload", response_model=PolicyUploadResponse)
async def upload_policy(
    file: UploadFile = File(..., description="PDF file of insurance policy")
):
    """
    Upload and process an insurance policy PDF.
    
    - **file**: PDF file containing the insurance policy
    
    Returns policy metadata and auto-generated policy ID.
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # Read file content
        pdf_content = await file.read()
        
        if len(pdf_content) == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded"
            )
        
        # Process policy
        policy_metadata = await policy_service.upload_policy(
            pdf_content, 
            file.filename
        )
        
        # Create summary
        summary = f"Processed {policy_metadata.total_pages} pages from {policy_metadata.insurance_company}"
        
        return PolicyUploadResponse(
            policy_id=policy_metadata.policy_id,
            insurance_company=policy_metadata.insurance_company,
            policy_holder=policy_metadata.policy_holder,
            policy_number=policy_metadata.policy_number,
            date_issued=policy_metadata.date_issued,
            total_pages=policy_metadata.total_pages,
            summary=summary,
            message="Policy uploaded and processed successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing policy: {str(e)}"
        )


@router.get("/{policy_id}/metadata")
async def get_policy_metadata(policy_id: str):
    """
    Get metadata for an uploaded policy.
    
    - **policy_id**: ID of the uploaded policy
    """
    policy_metadata = policy_service.get_policy_metadata(policy_id)
    
    if not policy_metadata:
        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )
    
    return policy_metadata