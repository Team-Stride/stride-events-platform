"""
Application configuration using Pydantic Settings.
Follows Stride Ahead standards for environment management.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Stride Events Platform"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Stride ID API Integration
    STRIDE_ID_API_URL: str
    STRIDE_ID_API_KEY: Optional[str] = None
    
    # SendGrid Email Service
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@strideahead.in"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    

    
    # Payment Gateway Settings
    RAZORPAY_KEY_ID: str = ""
    RAZORPAY_KEY_SECRET: str = ""
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    PAYMENT_WEBHOOK_SECRET: str = ""


    
    # WhatsApp (Karix) Settings
    KARIX_API_KEY: str = ""
    KARIX_SENDER_NUMBER: str = ""  # Your Karix WhatsApp number


    
    # Karix WhatsApp Settings
    KARIX_API_URL: str = "https://api.karix.io/v2"
    KARIX_API_KEY: str = ""
    KARIX_SENDER_NUMBER: str = ""  # Your Karix WhatsApp number

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
