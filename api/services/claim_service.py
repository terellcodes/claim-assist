"""
Claim Service

Simple service for handling claim submissions and evaluations.
"""

from typing import Dict, Any
from services.agents.claim_consultant import claim_consultant
from services.policy_service import policy_service
from models.schemas.claim import ClaimRequest, ClaimResponse


class ClaimService:
    """Simple service for claim operations."""
    
    def __init__(self):
        self.agent = claim_consultant
    
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
            
            # Parse agent response to determine status
            evaluation = result.get("response", "")
            claim_status = self._determine_claim_status(evaluation)
            
            # Extract email draft or suggestions
            email_draft = None
            suggestions = None
            
            if claim_status == "valid":
                email_draft = self._extract_email_draft(evaluation)
            else:
                suggestions = self._extract_suggestions(evaluation)
            
            return ClaimResponse(
                policy_id=claim_request.policy_id,
                claim_status=claim_status,
                evaluation=evaluation,
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
    
    def _determine_claim_status(self, evaluation: str) -> str:
        """Simple logic to determine claim status from agent response."""
        eval_lower = evaluation.lower()
        
        if any(word in eval_lower for word in ["valid", "covered", "approved", "eligible"]):
            return "valid"
        elif any(word in eval_lower for word in ["invalid", "not covered", "excluded", "denied"]):
            return "invalid"
        else:
            return "needs_review"
    
    def _extract_email_draft(self, evaluation: str) -> str:
        """Extract email draft from agent response (simple approach)."""
        # Look for email sections in the response
        lines = evaluation.split('\n')
        email_started = False
        email_lines = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ["subject:", "dear", "email", "draft"]):
                email_started = True
            
            if email_started:
                email_lines.append(line)
                
            # Stop if we hit the end marker
            if email_started and "best regards" in line.lower():
                break
        
        return '\n'.join(email_lines) if email_lines else evaluation
    
    def _extract_suggestions(self, evaluation: str) -> str:
        """Extract suggestions from agent response."""
        # For now, just return the full evaluation as suggestions
        # Could be enhanced to parse specific suggestion sections
        return evaluation


# Global service instance
claim_service = ClaimService()