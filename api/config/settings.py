from typing import List, Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "ClaimAssist API"
    APP_DESCRIPTION: str = "AI-powered insurance claim evaluation and drafting service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    
    # AI/ML API Keys
    OPENAI_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_PROJECT: str = "ClaimAssist"
    LANGSMITH_API_KEY: Optional[str] = None
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # Local frontend
        "http://127.0.0.1:3000",
        "https://*.vercel.app",   # Vercel preview deployments
        "https://claim-assist.vercel.app"  # Production frontend (update this with your actual domain)
    ]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True

    # Environment
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = [".env", "../.env"]  # Check current dir first, then parent
        case_sensitive = True

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def has_required_api_keys(self) -> bool:
        """Check if all required API keys are set."""
        required_keys = [self.OPENAI_API_KEY]
        return all(key is not None and key.strip() != "" for key in required_keys)
    
    def validate_api_keys(self) -> None:
        """Validate that required API keys are set."""
        missing_keys = []
        
        if not self.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        
        if missing_keys:
            keys_list = ", ".join(missing_keys)
            raise ValueError(
                f"Missing required API keys: {keys_list}. "
                f"Please set them in your .env file or environment variables."
            )
    
    def setup_environment_variables(self) -> None:
        """Set up environment variables for AI services."""
        import os
        
        # Set OpenAI API key if available
        if self.OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY
        
        # Set Tavily API key if available
        if self.TAVILY_API_KEY:
            os.environ["TAVILY_API_KEY"] = self.TAVILY_API_KEY
        
        # Set LangSmith tracing if enabled
        if self.LANGCHAIN_TRACING_V2.lower() == "true":
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = self.LANGCHAIN_PROJECT
            if self.LANGSMITH_API_KEY:
                os.environ["LANGSMITH_API_KEY"] = self.LANGSMITH_API_KEY


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache to prevent multiple reads of environment variables.
    Automatically sets up environment variables for AI services.
    """
    settings = Settings()
    
    # Set up environment variables for AI services
    settings.setup_environment_variables()
    
    return settings


def get_settings_with_validation() -> Settings:
    """
    Get settings with API key validation.
    Use this when you need to ensure all required keys are present.
    """
    settings = get_settings()
    settings.validate_api_keys()
    return settings 