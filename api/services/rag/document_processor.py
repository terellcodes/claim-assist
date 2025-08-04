"""
Simple Document Processor

Basic PDF processing and chunking for insurance policies.
Auto-generates policy IDs and handles the complete policy upload flow.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Dict, Any, Tuple
import tempfile
import os
import uuid


class SimpleDocumentProcessor:
    """
    Simple document processor for insurance policies.
    Handles PDF parsing and chunking.
    """
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def generate_policy_id(self, pdf_content: bytes, filename: str = None) -> str:
        """
        Generate a unique policy ID for each upload.
        Always creates a unique ID, allowing multiple uploads of the same PDF.
        
        Args:
            pdf_content: Raw PDF bytes
            filename: Optional filename for readability
            
        Returns:
            Unique policy ID string
        """
        # Always generate a unique UUID for each upload
        unique_id = str(uuid.uuid4())[:8]
        
        # Add filename component if provided for readability
        if filename:
            filename_clean = filename.replace('.pdf', '').replace(' ', '_')[:10]
            return f"policy_{filename_clean}_{unique_id}"
        else:
            return f"policy_{unique_id}"
    
    def process_pdf_with_id(self, pdf_content: bytes, filename: str = None) -> Tuple[str, List[Document], Dict[str, Any]]:
        """
        Complete PDF processing with auto-generated policy ID.
        
        Args:
            pdf_content: Raw PDF bytes
            filename: Optional PDF filename
            
        Returns:
            Tuple of (policy_id, document_chunks, metadata_dict)
        """
        # Generate policy ID
        policy_id = self.generate_policy_id(pdf_content, filename)
        
        # Process PDF
        chunks, metadata = self.process_pdf(pdf_content)
        
        # Add policy ID to metadata
        metadata["policy_id"] = policy_id
        
        return policy_id, chunks, metadata
    
    def process_pdf(self, pdf_content: bytes) -> Tuple[List[Document], Dict[str, Any]]:
        """
        Process PDF content into chunks and extract metadata.
        
        Args:
            pdf_content: Raw PDF bytes
            
        Returns:
            Tuple of (document_chunks, metadata_dict)
        """
        # Save to temporary file for PyPDFLoader
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(pdf_content)
            temp_path = temp_file.name
        
        try:
            # Load PDF
            loader = PyPDFLoader(temp_path, mode="single")
            documents = loader.load()
            
            # Extract basic metadata
            metadata = self._extract_metadata(documents)
            
            # Chunk documents
            chunks = self.text_splitter.split_documents(documents)
            
            return chunks, metadata
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _extract_metadata(self, documents: List[Document]) -> Dict[str, Any]:
        """
        Extract simple metadata from PDF documents.
        
        Args:
            documents: List of loaded documents
            
        Returns:
            Dictionary with extracted metadata
        """
        if not documents:
            return {}
        
        # Get metadata from first document
        doc_metadata = documents[0].metadata
        
        # Extract simple fields (keep it basic for now)
        metadata = {
            "total_pages": len(documents),
            "producer": doc_metadata.get("producer", "Unknown"),
            "creator": doc_metadata.get("creator", "Unknown"),
            "title": doc_metadata.get("title", "Insurance Policy"),
            "subject": doc_metadata.get("subject", ""),
        }
        
        # Try to extract policy info from content (very basic)
        content = documents[0].page_content if documents else ""
        metadata.update(self._extract_policy_info(content))
        
        return metadata
    
    def _extract_policy_info(self, content: str) -> Dict[str, Any]:
        """
        Extract basic policy information from content.
        Very simple pattern matching - can be improved later.
        
        Args:
            content: Document content
            
        Returns:
            Dictionary with policy info
        """
        policy_info = {
            "insurance_company": "Not specified",
            "policy_holder": "Not specified", 
            "policy_number": "Not specified",
            "date_issued": "Not specified",
        }
        
        # Simple pattern matching (can be enhanced later)
        content_upper = content.upper()
        
        # Look for common insurance company names
        companies = ["SHELTER", "STATE FARM", "ALLSTATE", "GEICO", "PROGRESSIVE"]
        for company in companies:
            if company in content_upper:
                policy_info["insurance_company"] = company.title()
                break
        
        # Look for policy number patterns (basic)
        import re
        policy_patterns = [
            r"POLICY\s*(?:NUMBER|NO\.?)\s*:?\s*([A-Z0-9\-]+)",
            r"POLICY\s+([A-Z0-9\-]{6,})",
        ]
        
        for pattern in policy_patterns:
            match = re.search(pattern, content_upper)
            if match:
                policy_info["policy_number"] = match.group(1)
                break
        
        return policy_info