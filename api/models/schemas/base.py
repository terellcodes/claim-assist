from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """Base schema for all models"""
    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseModel):
    """Base response schema with common fields."""
    success: bool = Field(default=True, description="Whether the operation was successful")
    message: str = Field(default="Operation completed successfully", description="Human-readable message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class ErrorResponse(BaseResponse):
    """Error response schema."""
    success: bool = Field(default=False, description="Always false for errors")  
    error_code: Optional[str] = Field(None, description="Error code for debugging")
    details: Optional[str] = Field(None, description="Additional error details")
