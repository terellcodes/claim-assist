"""
Claim Service

Simple service for handling claim submissions and evaluations.
"""

from typing import Dict, Any
from services.agents.claim_consultant import get_claim_consultant
from services.policy_service import policy_service
from models.schemas.claim import ClaimRequest, ClaimResponse


class ClaimService:
    """Simple service for claim operations."""
    
    def __init__(self):
        # Use lazy initialization - agent will be created when first needed
        self._agent = None
    
    @property
    def agent(self):
        """Lazy initialization of the claim consultant agent."""
        if self._agent is None:
            self._agent = get_claim_consultant()
        return self._agent
    
    async def submit_claim(self, claim_request: ClaimRequest) -> ClaimResponse:
        """
        Submit and evaluate a claim.
        
        Args:
            claim_request: Claim details from user
            
        Returns:
            ClaimResponse with evaluation results
        """
        # Verify policy exists
        policy_metadata = policy_service.get_policy_metadata(claim_request.policy_id)
        if not policy_metadata:
            return ClaimResponse(
                policy_id=claim_request.policy_id,
                claim_status="invalid",
                evaluation="Policy not found. Please upload your policy first.",
                success=False,
                message="Policy not found"
            )
        
        # Format claim description for agent
        formatted_claim = self._format_claim_description(claim_request)
        
        # Evaluate with agent
        try:
            result = self.agent.evaluate_claim(formatted_claim, claim_request.policy_id)
            
            # Agent now returns structured data - use it directly
            is_valid = result.get("is_valid", False)
            claim_status = "valid" if is_valid else "invalid"
            evaluation = result.get("evaluation", "")
            citations = result.get("citations")
            email_draft = result.get("email_draft")
            suggestions = result.get("suggestions")
            
            # Ensure citations is a list (convert string to list if needed)
            if isinstance(citations, str) and citations:
                citations = [citations]
            elif not citations:
                citations = None
            
            # Ensure suggestions is a list (convert string to list if needed)
            if isinstance(suggestions, str) and suggestions:
                suggestions = [suggestions]
            elif not suggestions:
                suggestions = None
            
            return ClaimResponse(
                policy_id=claim_request.policy_id,
                claim_status=claim_status,
                evaluation=evaluation,
                citations=citations,
                email_draft=email_draft,
                suggestions=suggestions,
                message="Claim evaluated successfully"
            )
            
        except Exception as e:
            return ClaimResponse(
                policy_id=claim_request.policy_id,
                claim_status="error",
                evaluation=f"Error evaluating claim: {str(e)}",
                success=False,
                message="Evaluation failed"
            )
    
    def _format_claim_description(self, claim_request: ClaimRequest) -> str:
        """Format claim request into natural language for the agent."""
        return f"""
On {claim_request.incident_date} {claim_request.incident_time or ''}, I experienced an incident at {claim_request.location}. 
Policy holder: {claim_request.policy_holder_name}

Description: {claim_request.description}

I would like to file a claim under my insurance policy and need help determining if this claim is valid based on my policy terms.
        """.strip()
    


# Global service instance
claim_service = ClaimService()