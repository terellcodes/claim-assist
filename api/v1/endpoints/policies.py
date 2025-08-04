"""
Policy Management Endpoints

Handles policy upload and management operations.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from models.schemas.policy import PolicyUploadResponse
from services.policy_service import policy_service

router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("/upload", response_model=PolicyUploadResponse)
async def upload_policy(file: UploadFile = File(...)):
    """
    Upload and process an insurance policy PDF.
    
    Args:
        file: PDF file to upload
        
    Returns:
        PolicyUploadResponse with extracted metadata
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Validate file size (10MB limit)
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB in bytes
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
    
    try:
        # Process the policy
        policy_metadata = await policy_service.upload_policy(content, file.filename)
        
        return PolicyUploadResponse(
            policy_id=policy_metadata.policy_id,
            insurance_company=policy_metadata.insurance_company,
            policy_holder=policy_metadata.policy_holder,
            policy_number=policy_metadata.policy_number,
            date_issued=policy_metadata.date_issued,
            total_pages=policy_metadata.total_pages,
            producer=policy_metadata.producer,
            creator=policy_metadata.creator,
            title=policy_metadata.title,
            subject=policy_metadata.subject,
            message="Policy uploaded and processed successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process policy: {str(e)}")


@router.get("/{policy_id}")
async def get_policy(policy_id: str):
    """
    Get policy metadata by ID.
    
    Args:
        policy_id: Policy identifier
        
    Returns:
        Policy metadata
    """
    policy_metadata = policy_service.get_policy_metadata(policy_id)
    if not policy_metadata:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    return policy_metadata