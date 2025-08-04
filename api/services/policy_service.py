"""
Policy Service

Simple service for handling policy uploads and processing.
"""

from typing import Tuple
from services.rag.document_processor import SimpleDocumentProcessor
from services.rag.vector_store import get_vector_store_manager
from models.schemas.policy import PolicyMetadata


class PolicyService:
    """Simple service for policy operations."""
    
    def __init__(self):
        self.document_processor = SimpleDocumentProcessor()
    
    async def upload_policy(self, pdf_content: bytes, filename: str = None) -> PolicyMetadata:
        """
        Upload and process a policy PDF.
        
        Args:
            pdf_content: Raw PDF bytes
            filename: Optional filename
            
        Returns:
            PolicyMetadata with extracted information
        """
        # Process PDF with auto-generated ID
        policy_id, chunks, metadata = self.document_processor.process_pdf_with_id(
            pdf_content, filename
        )
        
        # Store in vector database
        vector_store_manager = get_vector_store_manager()
        vector_store = vector_store_manager.create_policy_namespace(policy_id)
        vector_store.add_documents(chunks)
        
        # Convert to PolicyMetadata
        policy_metadata = PolicyMetadata(
            policy_id=policy_id,
            insurance_company=metadata.get("insurance_company", "Not specified"),
            policy_holder=metadata.get("policy_holder", "Not specified"),
            policy_number=metadata.get("policy_number", "Not specified"),
            date_issued=metadata.get("date_issued", "Not specified"),
            total_pages=metadata.get("total_pages", 0),
            producer=metadata.get("producer"),
            creator=metadata.get("creator"),
            title=metadata.get("title"),
            subject=metadata.get("subject")
        )
        
        return policy_metadata
    
    def get_policy_metadata(self, policy_id: str) -> PolicyMetadata:
        """
        Retrieve policy metadata by ID.
        (In production, this would come from a database)
        
        Args:
            policy_id: Policy identifier
            
        Returns:
            PolicyMetadata or None if not found
        """
        # For now, just check if vector store exists
        try:
            vector_store_manager = get_vector_store_manager()
            vector_store_manager.get_policy_store(policy_id)
            return PolicyMetadata(
                policy_id=policy_id,
                insurance_company="Unknown",
                policy_holder="Unknown", 
                policy_number="Unknown",
                date_issued="Unknown",
                total_pages=0
            )
        except Exception:
            return None


# Global service instance
policy_service = PolicyService()