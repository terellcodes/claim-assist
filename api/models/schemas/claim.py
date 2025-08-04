"""
Claim API Schemas

Simple Pydantic models for claim submission and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from .base import BaseResponse


class ClaimRequest(BaseModel):
    """Request schema for claim submission."""
    policy_id: str = Field(..., description="Policy ID from upload")
    policy_holder_name: str = Field(..., description="Name of policy holder")
    incident_date: str = Field(..., description="Date of incident (YYYY-MM-DD)")
    incident_time: Optional[str] = Field(None, description="Time of incident (HH:MM)")
    location: str = Field(..., description="Location where incident occurred")
    description: str = Field(..., description="Detailed description of the claim", min_length=10)
    retrieval_strategy: Literal["basic", "advanced_flashrank", "advanced_cohere"] = Field(
        default="basic", 
        description="Strategy for retrieving relevant policy information"
    )


class ClaimResponse(BaseResponse):
    """Response for claim evaluation."""
    policy_id: str = Field(..., description="Policy ID that was evaluated")
    claim_status: str = Field(..., description="Status: 'valid', 'invalid', or 'needs_review'")
    evaluation: str = Field(..., description="Detailed evaluation from AI agent")
    citations: Optional[List[str]] = Field(None, description="Citations from the policy that support the analysis")
    email_draft: Optional[str] = Field(None, description="Professional email draft if claim is valid")
    suggestions: Optional[List[str]] = Field(None, description="Suggestions for improvement if invalid")
    retrieval_strategy: str = Field(..., description="Strategy used for policy retrieval")
    processed_at: datetime = Field(default_factory=datetime.now, description="When claim was processed")


class ClaimSummary(BaseModel):
    """Simple claim summary for internal use."""
    policy_id: str
    incident_type: str
    incident_date: str
    location: str
    description_preview: str  # First 100 chars