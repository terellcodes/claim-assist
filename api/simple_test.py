#!/usr/bin/env python3
"""
Simple API Test

Test the core functionality with existing PDFs.
"""

import sys
import os
sys.path.append('.')

async def test_policy_upload():
    """Test policy upload with real PDF."""
    try:
        # Initialize settings first to set environment variables
        from config.settings import get_settings
        settings = get_settings()
        print(f"✅ Settings initialized: {settings.APP_NAME}")
        
        from services.policy_service import policy_service
        
        # Read a real PDF file
        pdf_path = "../notebooks/data/oklahoma_home_insurance_policy.pdf"
        
        if not os.path.exists(pdf_path):
            print(f"❌ PDF file not found: {pdf_path}")
            return
        
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        print(f"✅ PDF loaded: {len(pdf_content)} bytes")
        
        # Test policy upload
        policy_metadata = await policy_service.upload_policy(
            pdf_content, 
            "oklahoma_home_insurance_policy.pdf"
        )
        
        print("✅ Policy upload successful!")
        print(f"Policy ID: {policy_metadata.policy_id}")
        print(f"Insurance Company: {policy_metadata.insurance_company}")
        print(f"Policy Holder: {policy_metadata.policy_holder}")
        print(f"Policy Number: {policy_metadata.policy_number}")
        print(f"Total Pages: {policy_metadata.total_pages}")
        
        return policy_metadata.policy_id
        
    except Exception as e:
        print(f"❌ Policy upload failed: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_claim_submission(policy_id: str):
    """Test claim submission."""
    try:
        # Initialize settings first
        from config.settings import get_settings
        settings = get_settings()
        
        from services.claim_service import claim_service
        from models.schemas.claim import ClaimRequest
        
        # Create a test claim
        claim_request = ClaimRequest(
            policy_id=policy_id,
            policy_holder_name="John Doe",
            incident_date="2024-01-15",
            incident_time="14:30",
            location="123 Main St, Oklahoma City, OK",
            description="A severe hailstorm damaged my roof on January 15th. Several shingles were cracked and some were completely missing, causing water to leak into my attic. I have photographs of the damage and a quote from a roofing contractor for repairs."
        )
        
        print("✅ Testing claim submission...")
        
        # Submit claim
        result = await claim_service.submit_claim(claim_request)
        
        print("✅ Claim submission successful!")
        print(f"Claim Status: {result.claim_status}")
        print(f"Evaluation Preview: {result.evaluation[:200]}...")
        if result.email_draft:
            print("✅ Email draft generated")
        if result.suggestions:
            print("✅ Suggestions provided")
        
        return True
        
    except Exception as e:
        print(f"❌ Claim submission failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run the tests."""
    print("🚀 Testing ClaimAssist API")
    print("=" * 50)
    
    # Test policy upload
    policy_id = await test_policy_upload()
    
    if policy_id:
        print("\n" + "=" * 50)
        # Test claim submission
        await test_claim_submission(policy_id)
    
    print("\n✅ Test completed!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())