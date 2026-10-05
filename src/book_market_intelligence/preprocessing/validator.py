"""
Dataset schema validation, quality checks, and statistics reporting.
"""

from typing import Dict, Any, Tuple, Optional
import pandas as pd
import numpy as np
from book_market_intelligence.core.exceptions import PreprocessingError
from book_market_intelligence.core.logging import logger

VALID_SENTIMENTS = {"positive", "negative", "neutral"}


def validate_feedback_dataframe(
    df: pd.DataFrame,
    min_text_length: int = 3
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Validates and normalizes customer feedback dataset:
    1. Ensures clean_text column exists
    2. Drops null or blank texts
    3. Normalizes sentiment values to Title Case (Positive, Negative, Neutral)
    4. Constrains confidence to [0.0, 1.0]
    5. Deduplicates by clean_text
    6. Returns cleaned DataFrame and comprehensive quality report.
    """
    if df is None or not isinstance(df, pd.DataFrame):
        raise PreprocessingError("Input must be a valid pandas DataFrame")

    initial_rows = len(df)
    logger.info(f"Validating dataset with {initial_rows} initial rows...")

    # Normalize column names
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Support 'cleaned_text' or 'text' if clean_text is missing
    if "clean_text" not in df.columns:
        if "cleaned_text" in df.columns:
            df["clean_text"] = df["cleaned_text"]
        elif "text" in df.columns:
            df["clean_text"] = df["text"]
        else:
            raise PreprocessingError("Required column 'clean_text' is missing from dataset.")

    # 1. Null / Empty text cleaning
    df["clean_text"] = df["clean_text"].fillna("").astype(str).str.strip()
    df = df[df["clean_text"].str.len() >= min_text_length]

    # 2. Deduplication
    dup_count = int(df.duplicated(subset=["clean_text"]).sum())
    df = df.drop_duplicates(subset=["clean_text"]).reset_index(drop=True)

    # 3. Sentiment normalization
    if "sentiment" in df.columns:
        df["sentiment"] = (
            df["sentiment"]
            .fillna("neutral")
            .astype(str)
            .str.strip()
            .str.lower()
        )
        df["sentiment"] = df["sentiment"].map({
            "positive": "Positive",
            "negative": "Negative",
            "neutral": "Neutral"
        }).fillna("Neutral")
    else:
        df["sentiment"] = "Neutral"

    # 4. Confidence normalization
    if "confidence" in df.columns:
        df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce").fillna(0.7)
        df["confidence"] = df["confidence"].clip(0.0, 1.0)
    else:
        df["confidence"] = 0.75

    # 5. Metadata columns defaults if missing
    if "source" not in df.columns:
        df["source"] = "consumer_feedback"

    if "topic" not in df.columns:
        df["topic"] = "general_reading"

    if "aspect" not in df.columns:
        df["aspect"] = "unspecified"

    # Metrics
    text_lengths = df["clean_text"].str.len()
    sentiment_dist = df["sentiment"].value_counts().to_dict()

    stats = {
        "initial_rows": initial_rows,
        "valid_rows": len(df),
        "duplicates_removed": dup_count,
        "min_char_length": int(text_lengths.min()) if not df.empty else 0,
        "max_char_length": int(text_lengths.max()) if not df.empty else 0,
        "avg_char_length": round(float(text_lengths.mean()), 2) if not df.empty else 0.0,
        "sentiment_distribution": sentiment_dist
    }

    logger.info(f"Validation complete: {len(df)} records valid ({dup_count} duplicates removed).")
    return df, stats
