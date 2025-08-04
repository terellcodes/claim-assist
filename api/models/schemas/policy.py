"""
Policy API Schemas

Simple Pydantic models for policy upload and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseResponse


class PolicyUploadResponse(BaseResponse):
    """Response for successful policy upload."""
    policy_id: str = Field(..., description="Auto-generated policy ID")
    insurance_company: str = Field(..., description="Detected insurance company")
    policy_holder: str = Field(..., description="Policy holder name")
    policy_number: str = Field(..., description="Policy number")
    date_issued: str = Field(..., description="Policy issue date")
    total_pages: int = Field(..., description="Number of pages processed")
    summary: str = Field(..., description="Brief policy summary")


class PolicyMetadata(BaseModel):
    """Policy metadata extracted from PDF."""
    policy_id: str
    insurance_company: str
    policy_holder: str
    policy_number: str
    date_issued: str
    total_pages: int
    producer: Optional[str] = None
    creator: Optional[str] = None
    title: Optional[str] = None
    subject: Optional[str] = None