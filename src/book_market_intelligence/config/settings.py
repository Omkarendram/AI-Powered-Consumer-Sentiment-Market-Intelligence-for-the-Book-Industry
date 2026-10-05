"""
Enterprise configuration and settings management.
"""

import os
from pathlib import Path
# Resolve repository root directory reliably from this file location
# This file: src/book_market_intelligence/config/settings.py -> 3 levels up to repo root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass


class Settings:
    """
    Centralized configuration class with type-safe property accessors
    and environment variable overrides.
    """

    def __init__(self) -> None:
        # Paths
        self.PROJECT_ROOT: Path = PROJECT_ROOT
        self.DATA_DIR: Path = PROJECT_ROOT / "data"
        self.RAW_DATA_DIR: Path = self.DATA_DIR / "raw"
        self.PROCESSED_DATA_DIR: Path = self.DATA_DIR / "processed"
        self.VECTOR_DB_DIR: Path = self.DATA_DIR / "vectorstore"
        self.USERS_FILE: Path = self.DATA_DIR / "users.json"
        self.DOCS_DIR: Path = PROJECT_ROOT / "docs"

        # Ensure essential directories exist
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Environment & Server
        self.APP_ENV: str = os.getenv("APP_ENV", "development").lower()
        self.APP_DEBUG: bool = os.getenv("APP_DEBUG", "false").lower() in ("true", "1", "yes")
        self.PORT: int = int(os.getenv("PORT", 8000))
        self.HOST: str = os.getenv("HOST", "0.0.0.0")

        # Groq LLM API
        self.GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
        self.GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.GROQ_FALLBACK_MODEL: str = os.getenv("GROQ_FALLBACK_MODEL", "llama-3.1-8b-instant")

        # Data Scraping Keys
        self.NEWS_API_KEY: Optional[str] = os.getenv("NEWS_API_KEY")
        self.YOUTUBE_API_KEY: Optional[str] = os.getenv("YOUTUBE_API_KEY")

        # Security & Authentication
        self.AUTH_SECRET_SALT: str = os.getenv(
            "AUTH_SECRET_SALT", "enterprise_book_intel_salt_default_key"
        )
        self.PASSWORD_MIN_LENGTH: int = int(os.getenv("PASSWORD_MIN_LENGTH", 4))

        # Alerting & Notifications
        self.ALERT_EMAIL: Optional[str] = os.getenv("ALERT_EMAIL")
        self.ALERT_PASSWORD: Optional[str] = os.getenv("ALERT_PASSWORD")
        self.ALERT_RECEIVER: Optional[str] = os.getenv("ALERT_RECEIVER")
        self.ALERT_SMTP_SERVER: str = os.getenv("ALERT_SMTP_SERVER", "smtp.gmail.com")
        self.ALERT_SMTP_PORT: int = int(os.getenv("ALERT_SMTP_PORT", 465))

        # RAG Settings
        self.EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.RAG_TOP_K: int = int(os.getenv("RAG_TOP_K", 6))

    # Standard Dataset Paths
    @property
    def raw_youtube_path(self) -> Path:
        return self.RAW_DATA_DIR / "youtube_book_comments.csv"

    @property
    def raw_news_path(self) -> Path:
        return self.RAW_DATA_DIR / "news_articles.csv"

    @property
    def raw_ecommerce_path(self) -> Path:
        return self.RAW_DATA_DIR / "ecommerce_books.csv"

    @property
    def processed_cleaned_text_path(self) -> Path:
        return self.PROCESSED_DATA_DIR / "cleaned_text.csv"

    @property
    def processed_feedback_path(self) -> Path:
        return self.PROCESSED_DATA_DIR / "book_feedback.csv"

    @property
    def processed_sentiment_results_path(self) -> Path:
        return self.PROCESSED_DATA_DIR / "sentiment_analysis_results_batch.csv"

    @property
    def processed_topics_path(self) -> Path:
        return self.PROCESSED_DATA_DIR / "book_market_sentiment_topics.csv"


# Singleton settings instance
settings = Settings()
