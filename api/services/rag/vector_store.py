"""
Simple Vector Store Setup

Basic Qdrant integration with namespace support for ClaimAssist.
Keeps it simple - no complex features yet.
"""

from langchain_qdrant import QdrantVectorStore
from langchain_openai.embeddings import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from typing import List
import uuid


class SimpleVectorStore:
    """
    Simple vector store wrapper for policy documents.
    Each policy gets its own namespace (collection).
    """
    
    def __init__(self):
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        self.embedding_dim = 1536
        self.client = QdrantClient(":memory:")  # Simple in-memory for now
        
    def create_policy_namespace(self, policy_id: str) -> QdrantVectorStore:
        """
        Create a new collection for a policy.
        
        Args:
            policy_id: Unique identifier for the policy
            
        Returns:
            QdrantVectorStore configured for this policy
        """
        collection_name = f"policy_{policy_id}"
        
        # Create collection if it doesn't exist
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=self.embedding_dim, distance=Distance.COSINE),
        )
        
        # Return configured vector store
        return QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=self.embedding_model,
        )
    
    def get_policy_store(self, policy_id: str) -> QdrantVectorStore:
        """
        Get existing vector store for a policy.
        
        Args:
            policy_id: Policy identifier
            
        Returns:
            QdrantVectorStore for the policy
        """
        collection_name = f"policy_{policy_id}"
        
        return QdrantVectorStore(
            client=self.client,
            collection_name=collection_name,
            embedding=self.embedding_model,
        )
    
    def generate_policy_id(self) -> str:
        """Generate a simple unique policy ID."""
        return str(uuid.uuid4())


# Global instance - lazy initialization to avoid API key issues at import time
_vector_store_manager = None


def get_vector_store_manager() -> SimpleVectorStore:
    """Get the global vector store manager instance (lazy initialization)."""
    global _vector_store_manager
    if _vector_store_manager is None:
        _vector_store_manager = SimpleVectorStore()
    return _vector_store_manager