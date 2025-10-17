from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    APP_NAME: str = "AI-DiReksi"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ai_direksi"
    DATABASE_TEST_URL: Optional[str] = None
    
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    TWITTER_BEARER_TOKEN: Optional[str] = None
    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None
    FACEBOOK_APP_ID: Optional[str] = None
    FACEBOOK_APP_SECRET: Optional[str] = None
    
    NLP_MODEL: str = "id_core_news_md"
    SENTIMENT_THRESHOLD_NEGATIVE: float = 0.3
    SENTIMENT_THRESHOLD_POSITIVE: float = 0.6
    
    SELENIUM_DRIVER_PATH: str = "/usr/local/bin/chromedriver"
    SCRAPING_TIMEOUT: int = 30
    MAX_SCRAPING_PAGES: int = 10
    
    ENCRYPTION_KEY: str = "your-encryption-key-change-this"
    DATA_RETENTION_DAYS: int = 90
    
    MAX_UPLOAD_SIZE: int = 10485760
    UPLOAD_DIR: str = "./uploads"
    
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: str = "noreply@ai-direksi.go.id"
    
    REDIS_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
