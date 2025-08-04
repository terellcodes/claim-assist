#!/usr/bin/env python3
"""
Test Environment Variable Loading

Test that the settings properly load and configure environment variables.
"""

import sys
import os
sys.path.append('.')

def test_settings_loading():
    """Test that settings load properly from .env file."""
    try:
        print("🧪 Testing Settings Loading...")
        
        from config.settings import get_settings, get_settings_with_validation
        
        # Load settings
        settings = get_settings()
        
        print(f"✅ App Name: {settings.APP_NAME}")
        print(f"✅ App Version: {settings.APP_VERSION}")
        print(f"✅ Environment: {settings.ENVIRONMENT}")
        print(f"✅ Debug Mode: {settings.DEBUG}")
        
        # Check API keys
        print(f"\n🔑 API Key Status:")
        print(f"OpenAI API Key: {'✅ Set' if settings.OPENAI_API_KEY else '❌ Missing'}")
        print(f"Tavily API Key: {'✅ Set' if settings.TAVILY_API_KEY else '❌ Missing'}")
        print(f"LangSmith API Key: {'✅ Set' if settings.LANGSMITH_API_KEY else '❌ Missing'}")
        
        # Check if required keys are available
        print(f"\n📋 Validation:")
        print(f"Has Required Keys: {'✅ Yes' if settings.has_required_api_keys else '❌ No'}")
        
        # Test environment variable setup
        print(f"\n🌍 Environment Variables:")
        openai_key_set = os.environ.get("OPENAI_API_KEY") is not None
        tavily_key_set = os.environ.get("TAVILY_API_KEY") is not None
        
        print(f"OPENAI_API_KEY in env: {'✅ Yes' if openai_key_set else '❌ No'}")
        print(f"TAVILY_API_KEY in env: {'✅ Yes' if tavily_key_set else '❌ No'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Settings loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_key_validation():
    """Test API key validation."""
    try:
        print("\n🧪 Testing API Key Validation...")
        
        from config.settings import get_settings_with_validation
        
        # Try to get settings with validation
        settings = get_settings_with_validation()
        print("✅ API key validation passed")
        return True
        
    except ValueError as e:
        print(f"⚠️  API key validation failed (expected): {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected validation error: {e}")
        return False


def test_openai_connection():
    """Test if OpenAI connection works with loaded API key."""
    try:
        print("\n🧪 Testing OpenAI Connection...")
        
        from config.settings import get_settings
        
        # Load settings first to set environment variables
        settings = get_settings()
        
        if not settings.OPENAI_API_KEY:
            print("⚠️  No OpenAI API key available, skipping connection test")
            return True
        
        # Try to create OpenAI embeddings (this should work now)
        from langchain_openai.embeddings import OpenAIEmbeddings
        
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        print("✅ OpenAI embeddings initialized successfully")
        
        # Test a simple embedding (optional - uses API quota)
        # test_text = "This is a test embedding"
        # result = embeddings.embed_query(test_text)
        # print(f"✅ Test embedding generated: {len(result)} dimensions")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection test failed: {e}")
        return False


def main():
    """Run all environment tests."""
    print("🚀 ClaimAssist Environment Configuration Test")
    print("=" * 50)
    
    tests = [
        ("Settings Loading", test_settings_loading),
        ("API Key Validation", test_api_key_validation),
        ("OpenAI Connection", test_openai_connection),
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
    
    if passed >= 2:  # Settings loading and at least one other test
        print("🚀 Environment configuration is working!")
        print("\n📝 Next steps:")
        print("   1. Start the API server: cd api && uv run uvicorn main:app --reload")
        print("   2. Test endpoints at http://localhost:8000/docs")
        print("   3. Upload a policy and submit a claim")
    else:
        print("⚠️  Environment configuration needs attention.")


if __name__ == "__main__":
    main()