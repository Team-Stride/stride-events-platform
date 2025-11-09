"""
Application configuration using Pydantic Settings.
Follows Stride Ahead standards for environment management.
"""
from pydantic_settings import BaseSettings
from pydantic import validator, Field
from typing import Optional, List
import secrets


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "Stride Events Platform"
    ENVIRONMENT: str = Field(default="development", description="Environment: development, staging, production")
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = Field(default=False, description="Debug mode")
    
    # Database
    DATABASE_URL: str = Field(..., description="PostgreSQL database URL")
    
    # Multi-tenancy
    TENANT_ID: str = Field(default="stride-ahead", description="Default tenant ID")
    
    # JWT Authentication
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32), description="JWT secret key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Stride ID API Integration
    STRIDE_ID_API_URL: str = Field(default="https://api.strideahead.in/v1", description="Stride ID API base URL")
    STRIDE_ID_API_KEY: Optional[str] = Field(default=None, description="Stride ID API key")
    STRIDE_ID_VALIDATION_URL: Optional[str] = Field(default=None, description="Stride ID token validation endpoint")
    JWT_SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32), description="JWT secret key for local validation")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    
    # SendGrid Email Service
    SENDGRID_API_KEY: Optional[str] = Field(default=None, description="SendGrid API key")
    SENDGRID_FROM_EMAIL: str = Field(default="noreply@strideahead.in", description="From email address")
    SENDGRID_FROM_NAME: str = Field(default="Stride Ahead", description="From name")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Payment Gateway Settings
    RAZORPAY_KEY_ID: str = Field(default="", description="Razorpay key ID")
    RAZORPAY_KEY_SECRET: str = Field(default="", description="Razorpay key secret")
    STRIPE_SECRET_KEY: str = Field(default="", description="Stripe secret key")
    STRIPE_PUBLISHABLE_KEY: str = Field(default="", description="Stripe publishable key")
    PAYMENT_WEBHOOK_SECRET: str = Field(default="", description="Payment webhook secret")
    PAYMENT_GATEWAY: str = Field(default="razorpay", description="Default payment gateway: razorpay or stripe")
    
    @validator("PAYMENT_GATEWAY")
    def validate_payment_gateway(cls, v):
        if v not in ["razorpay", "stripe"]:
            raise ValueError("PAYMENT_GATEWAY must be either 'razorpay' or 'stripe'")
        return v
    
    # WhatsApp (Karix) Settings
    KARIX_API_URL: str = Field(default="https://api.karix.io/v2", description="Karix API base URL")
    KARIX_API_KEY: str = Field(default="", description="Karix API key")
    KARIX_SENDER_NUMBER: str = Field(default="", description="Karix WhatsApp sender number (with country code)")
    
    # Frontend URLs
    FRONTEND_URL: str = Field(default="http://localhost:5173", description="Frontend base URL")
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = Field(default=5 * 1024 * 1024, description="Max upload size in bytes (default 5MB)")
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=["pdf", "doc", "docx", "jpg", "jpeg", "png"],
        description="Allowed file extensions"
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="API rate limit per minute")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()
    
    # Redis (for caching and rate limiting)
    REDIS_URL: Optional[str] = Field(default=None, description="Redis URL for caching")
    
    # Celery (for background tasks)
    CELERY_BROKER_URL: Optional[str] = Field(default=None, description="Celery broker URL")
    CELERY_RESULT_BACKEND: Optional[str] = Field(default=None, description="Celery result backend")
    
    # S3 / Object Storage (for file uploads)
    S3_BUCKET_NAME: Optional[str] = Field(default=None, description="S3 bucket name")
    S3_ACCESS_KEY: Optional[str] = Field(default=None, description="S3 access key")
    S3_SECRET_KEY: Optional[str] = Field(default=None, description="S3 secret key")
    S3_REGION: str = Field(default="ap-south-1", description="S3 region")
    S3_ENDPOINT_URL: Optional[str] = Field(default=None, description="S3 endpoint URL (for MinIO, etc.)")
    
    # Feature Flags
    ENABLE_REGISTRATION: bool = Field(default=True, description="Enable event registration")
    ENABLE_PAYMENTS: bool = Field(default=True, description="Enable payment processing")
    ENABLE_EMAIL_NOTIFICATIONS: bool = Field(default=True, description="Enable email notifications")
    ENABLE_WHATSAPP_NOTIFICATIONS: bool = Field(default=True, description="Enable WhatsApp notifications")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT.lower() == "production"
    
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.ENVIRONMENT.lower() == "development"


settings = Settings()


# Validation on startup
def validate_settings():
    """Validate critical settings on application startup"""
    errors = []
    
    if settings.ENABLE_PAYMENTS:
        if settings.PAYMENT_GATEWAY == "razorpay":
            if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
                errors.append("Razorpay credentials are required when ENABLE_PAYMENTS=True and PAYMENT_GATEWAY=razorpay")
        elif settings.PAYMENT_GATEWAY == "stripe":
            if not settings.STRIPE_SECRET_KEY:
                errors.append("Stripe credentials are required when ENABLE_PAYMENTS=True and PAYMENT_GATEWAY=stripe")
    
    if settings.ENABLE_EMAIL_NOTIFICATIONS:
        if not settings.SENDGRID_API_KEY:
            errors.append("SendGrid API key is required when ENABLE_EMAIL_NOTIFICATIONS=True")
    
    if settings.ENABLE_WHATSAPP_NOTIFICATIONS:
        if not settings.KARIX_API_KEY or not settings.KARIX_SENDER_NUMBER:
            errors.append("Karix credentials are required when ENABLE_WHATSAPP_NOTIFICATIONS=True")
    
    if not settings.DATABASE_URL:
        errors.append("DATABASE_URL is required")
    
    if errors:
        error_msg = "\n".join([f"  - {error}" for error in errors])
        raise ValueError(f"Configuration validation failed:\n{error_msg}")
    
    return True
