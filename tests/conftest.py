"""
Pytest configuration and global fixtures.
"""

import sys
from pathlib import Path
import pytest
import pandas as pd

# Add src to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@pytest.fixture
def sample_feedback_df() -> pd.DataFrame:
    """Provides a controlled test dataset of consumer feedback."""
    return pd.DataFrame({
        "clean_text": [
            "the book was absolutely amazing and inspiring to read",
            "terrible binding and pages were completely torn and damaged",
            "good book with practical advice on building habits",
            "boring repetitive content waste of money",
            "could you recommend another book on mythology",
            "the book was absolutely amazing and inspiring to read"  # duplicate
        ],
        "sentiment": ["positive", "negative", "positive", "negative", "neutral", "positive"],
        "confidence": [0.90, 0.85, 0.80, 0.78, 0.60, 0.90],
        "source": ["youtube", "ecommerce", "youtube", "news", "youtube", "youtube"],
        "topic": ["story_quality", "delivery", "story_quality", "pricing", "general_reading", "story_quality"],
        "aspect": ["inspiring read", "damaged binding", "practical advice", "waste of money", "book recommendation", "inspiring read"]
    })


@pytest.fixture
def temp_user_store(tmp_path: Path):
    """Provides an isolated AuthService instance with temporary storage."""
    from book_market_intelligence.auth.service import AuthService
    db_path = tmp_path / "test_users.json"
    service = AuthService(storage_path=db_path)
    return service
