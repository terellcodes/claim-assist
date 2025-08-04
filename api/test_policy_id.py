#!/usr/bin/env python3
"""
Test Policy ID Generation

Simple test to verify policy ID auto-generation works correctly.
"""

from services.rag.document_processor import SimpleDocumentProcessor


def test_policy_id_generation():
    """Test that policy IDs are generated correctly."""
    processor = SimpleDocumentProcessor()
    
    # Test with sample content
    sample_pdf_content = b"Sample PDF content for testing"
    
    # Test basic generation
    policy_id1 = processor.generate_policy_id(sample_pdf_content)
    policy_id2 = processor.generate_policy_id(sample_pdf_content)
    
    print(f"Generated Policy ID 1: {policy_id1}")
    print(f"Generated Policy ID 2: {policy_id2}")
    print(f"IDs are consistent: {policy_id1 == policy_id2}")
    
    # Test with filename
    policy_id_with_filename = processor.generate_policy_id(
        sample_pdf_content, 
        "Oklahoma Home Insurance Policy.pdf"
    )
    print(f"Policy ID with filename: {policy_id_with_filename}")
    
    # Test different content gives different ID
    different_content = b"Different PDF content for testing"
    different_policy_id = processor.generate_policy_id(different_content)
    print(f"Different content ID: {different_policy_id}")
    print(f"Different IDs: {policy_id1 != different_policy_id}")


if __name__ == "__main__":
    test_policy_id_generation()