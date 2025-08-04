#!/usr/bin/env python3
"""
Basic API Test

Test the core functionality without requiring API keys.
"""

import sys
import os
sys.path.append('.')

def test_imports():
    """Test that all imports work correctly."""
    try:
        print("Testing imports...")
        
        # Test document processor import
        from services.rag.document_processor import SimpleDocumentProcessor
        print("✅ Document processor import successful")
        
        # Test policy ID generation
        processor = SimpleDocumentProcessor()
        test_content = b"Sample PDF content for testing policy ID generation"
        policy_id = processor.generate_policy_id(test_content, "test_policy.pdf")
        print(f"✅ Policy ID generation works: {policy_id}")
        
        # Test schemas
        from models.schemas.policy import PolicyMetadata
        from models.schemas.claim import ClaimRequest, ClaimResponse
        from models.schemas.base import BaseResponse
        print("✅ All schemas import successfully")
        
        # Test API endpoints import
        from api.v1.endpoints.policies import router as policies_router
        from api.v1.endpoints.claims import router as claims_router
        from api.v1.endpoints.health import router as health_router
        print("✅ All endpoint routers import successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pdf_processing():
    """Test PDF processing logic without external dependencies."""
    try:
        print("\nTesting PDF processing...")
        
        from services.rag.document_processor import SimpleDocumentProcessor
        
        processor = SimpleDocumentProcessor()
        
        # Test different policy ID generation scenarios
        content1 = b"Sample PDF content #1"
        content2 = b"Sample PDF content #2"
        
        id1 = processor.generate_policy_id(content1, "home_policy.pdf") 
        id2 = processor.generate_policy_id(content1, "home_policy.pdf")  # Same content
        id3 = processor.generate_policy_id(content2, "auto_policy.pdf")  # Different content
        
        print(f"Policy ID 1: {id1}")
        print(f"Policy ID 2: {id2}")
        print(f"Policy ID 3: {id3}")
        
        # Verify consistency
        assert id1 == id2, "Same content should generate same ID"
        assert id1 != id3, "Different content should generate different IDs"
        
        print("✅ Policy ID generation is consistent and unique")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_schema_validation():
    """Test Pydantic schema validation."""
    try:
        print("\nTesting schema validation...")
        
        from models.schemas.claim import ClaimRequest
        from models.schemas.policy import PolicyMetadata
        
        # Test valid claim request
        valid_claim = ClaimRequest(
            policy_id="policy_test_12345",
            policy_holder_name="John Doe",
            incident_date="2024-01-15", 
            incident_time="14:30",
            location="123 Main St",
            description="Test claim description that is longer than minimum length"
        )
        
        print(f"✅ Valid claim created: {valid_claim.policy_id}")
        
        # Test policy metadata
        policy_meta = PolicyMetadata(
            policy_id="policy_test_12345",
            insurance_company="Test Insurance Co",
            policy_holder="John Doe",
            policy_number="POL-123456",
            date_issued="2024-01-01",
            total_pages=10
        )
        
        print(f"✅ Policy metadata created: {policy_meta.insurance_company}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema validation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_actual_pdf():
    """Test with real PDF file (metadata extraction only)."""
    try:
        print("\nTesting with real PDF...")
        
        from services.rag.document_processor import SimpleDocumentProcessor
        
        # Find a PDF file
        pdf_path = "../notebooks/data/oklahoma_home_insurance_policy.pdf"
        
        if not os.path.exists(pdf_path):
            print("⚠️  PDF file not found, skipping real PDF test")
            return True
        
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        print(f"✅ PDF loaded: {len(pdf_content)} bytes")
        
        processor = SimpleDocumentProcessor()
        
        # Generate policy ID
        policy_id = processor.generate_policy_id(pdf_content, "oklahoma_home_insurance_policy.pdf")
        print(f"✅ Generated policy ID: {policy_id}")
        
        # Test metadata extraction (basic)
        test_content = "SHELTER INSURANCE COMPANIES Policy Number: HO-123456 John Smith"
        metadata = processor._extract_policy_info(test_content)
        print(f"✅ Metadata extraction: {metadata}")
        
        return True
        
    except Exception as e:
        print(f"❌ Real PDF test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all basic tests."""
    print("🚀 Basic ClaimWise API Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("PDF Processing Test", test_pdf_processing), 
        ("Schema Validation Test", test_schema_validation),
        ("Real PDF Test", test_actual_pdf),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🚀 All basic tests passed! API structure is working correctly.")
        print("\n📝 Next steps:")
        print("   1. Set OPENAI_API_KEY and TAVILY_API_KEY environment variables")
        print("   2. Start the FastAPI server with: uvicorn main:app --reload")
        print("   3. Test endpoints at http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Please fix the issues before proceeding.")


if __name__ == "__main__":
    main()