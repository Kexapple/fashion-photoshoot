"""
Configuration and environment variables
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Firebase
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_PRIVATE_KEY_ID: str = os.getenv("FIREBASE_PRIVATE_KEY_ID", "")
    FIREBASE_PRIVATE_KEY: str = os.getenv("FIREBASE_PRIVATE_KEY", "")
    FIREBASE_CLIENT_EMAIL: str = os.getenv("FIREBASE_CLIENT_EMAIL", "")
    FIREBASE_CLIENT_ID: str = os.getenv("FIREBASE_CLIENT_ID", "")
    FIREBASE_AUTH_URI: str = os.getenv("FIREBASE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth")
    FIREBASE_TOKEN_URI: str = os.getenv("FIREBASE_TOKEN_URI", "https://oauth2.googleapis.com/token")
    FIREBASE_STORAGE_BUCKET: str = os.getenv("FIREBASE_STORAGE_BUCKET", "")
    
    # Nano Banana API
    NANO_BANANA_API_KEY: str = os.getenv("NANO_BANANA_API_KEY", "")
    NANO_BANANA_MODEL_ID: str = os.getenv("NANO_BANANA_MODEL_ID", "")
    
    # JazzCash / EasyPaisa
    JAZZCASH_MERCHANT_ID: str = os.getenv("JAZZCASH_MERCHANT_ID", "")
    JAZZCASH_PASSWORD: str = os.getenv("JAZZCASH_PASSWORD", "")
    JAZZCASH_INTEGRITY_KEY: str = os.getenv("JAZZCASH_INTEGRITY_KEY", "")
    
    EASYPAISA_MERCHANT_ID: str = os.getenv("EASYPAISA_MERCHANT_ID", "")
    EASYPAISA_PASSWORD: str = os.getenv("EASYPAISA_PASSWORD", "")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        os.getenv("FRONTEND_URL", "https://yourdomain.vercel.app")
    ]
    
    # Credit system
    FREE_TRIAL_LIMIT: int = 3  # 3 free generations per IP
    FIRST_LOGIN_BONUS: int = 5  # 5 free credits at first login
    
    # Rate limiting
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 10
    
    # Backend API
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
