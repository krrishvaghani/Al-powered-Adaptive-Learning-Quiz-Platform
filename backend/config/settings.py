import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Application settings
    APP_NAME: str = "AI-Powered Adaptive Learning & Quiz Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database settings
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "cursorai_db")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # OpenAI settings (for future integration)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # CORS settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    # Security settings
    PASSWORD_MIN_LENGTH: int = 8
    EMAIL_VERIFICATION_REQUIRED: bool = False
    
    # Quiz settings
    DEFAULT_QUIZ_QUESTIONS: int = 10
    MAX_QUIZ_QUESTIONS: int = 50
    QUIZ_TIME_LIMIT_MINUTES: int = 30

# Create settings instance
settings = Settings() 