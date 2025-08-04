from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from config.settings import get_settings, Settings
from utils.constants import ResponseMessage, StatusCode
from api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    print("🚀 Starting ClaimWise API...")
    
    # Initialize and validate settings
    try:
        settings = get_settings()
        print(f"✅ Settings loaded: {settings.APP_NAME} v{settings.APP_VERSION}")
        
        # Validate API keys (but don't fail if missing in development)
        if settings.has_required_api_keys:
            print("✅ All required API keys are configured")
        else:
            if settings.is_development:
                print("⚠️  Some API keys missing - functionality may be limited")
            else:
                print("❌ Missing required API keys in production!")
                
    except Exception as e:
        print(f"❌ Settings initialization failed: {e}")
        if not get_settings().is_development:
            raise  # Fail in production, but allow development to continue
    
    print("✅ ClaimWise API startup complete")
    yield
    
    # Shutdown
    print("👋 Shutting down ClaimWise API...")


def create_application() -> FastAPI:
    """
    Factory function to create and configure the FastAPI application.
    """
    settings = get_settings()
    
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        lifespan=lifespan,
        root_path="/api" if not settings.DEBUG else ""  # Add root_path for production
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    # Include API routes
    app.include_router(api_router, prefix="/api")

    return app


app = create_application()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": ResponseMessage.SUCCESS,
        "code": StatusCode.HTTP_200_OK,
        "message": "API is healthy"
    }


@app.get("/api/info")
async def get_api_info(settings: Settings = Depends(get_settings)):
    """Example endpoint using settings"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "debug_mode": settings.DEBUG
    }

# Handler for Vercel serverless
handler = Mangum(app)
