"""
Unit tests for text preprocessing, cleaner, and schema validator.
"""

import pandas as pd
from book_market_intelligence.preprocessing.cleaner import clean_text
from book_market_intelligence.preprocessing.validator import validate_feedback_dataframe


def test_clean_text_removes_urls_and_punctuation():
    raw = "Check out https://books.com/review! Amazing story with great characters..."
    cleaned = clean_text(raw, remove_stopwords=False)
    assert "https" not in cleaned
    assert "books.com" not in cleaned
    assert "!" not in cleaned
    assert "amazing story with great characters" in cleaned


def test_clean_text_stopword_removal():
    raw = "this is a very good book and i loved reading it"
    cleaned = clean_text(raw, remove_stopwords=True)
    # Stopwords like 'this', 'is', 'a', 'very', 'and', 'i', 'it' should be stripped
    tokens = cleaned.split()
    assert "very" not in tokens
    assert "good" in tokens
    assert "book" in tokens
    assert "loved" in tokens


def test_clean_text_empty_and_none():
    assert clean_text("") == ""
    assert clean_text(None) == ""
    assert clean_text("   \n\t  ") == ""


def test_validate_feedback_dataframe(sample_feedback_df):
    cleaned_df, stats = validate_feedback_dataframe(sample_feedback_df)

    # Initial had 6 rows (1 duplicate), so valid rows should be 5
    assert stats["valid_rows"] == 5
    assert stats["duplicates_removed"] == 1
    assert "clean_text" in cleaned_df.columns
    assert "sentiment" in cleaned_df.columns
    assert "confidence" in cleaned_df.columns

    # Sentiment normalized to title case
    assert set(cleaned_df["sentiment"].unique()).issubset({"Positive", "Negative", "Neutral"})

    # Confidences within [0.0, 1.0]
    assert (cleaned_df["confidence"] >= 0.0).all()
    assert (cleaned_df["confidence"] <= 1.0).all()
