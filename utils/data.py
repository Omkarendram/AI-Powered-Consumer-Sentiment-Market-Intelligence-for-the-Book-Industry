"""
Data loading and enrichment utility functions.
"""

from pathlib import Path
from typing import Optional
import numpy as np
import pandas as pd
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger


def load_book_data(custom_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Loads processed consumer feedback dataset with fallback resolution and
    ensures simulated business dimensions (store, region, category, sales)
    exist with deterministic distributions for multi-persona dashboard exploration.
    """
    candidates = [
        custom_path,
        settings.processed_topics_path,
        settings.processed_feedback_path,
        settings.processed_sentiment_results_path,
        settings.processed_cleaned_text_path
    ]

    target = None
    for cand in candidates:
        if cand and cand.exists():
            target = cand
            break

    if target is None:
        logger.warning("No processed dataset found. Returning empty structured DataFrame.")
        return pd.DataFrame(columns=["clean_text", "sentiment", "confidence", "store", "region", "category", "sales", "date"])

    df = pd.read_csv(target)

    # 1. Standardize Sentiment
    if "sentiment" not in df.columns:
        df["sentiment"] = "Neutral"
    else:
        df["sentiment"] = (
            df["sentiment"]
            .fillna("neutral")
            .astype(str)
            .str.strip()
            .str.title()
        )
        df["sentiment"] = df["sentiment"].map({
            "Positive": "Positive",
            "Negative": "Negative",
            "Neutral": "Neutral"
        }).fillna("Neutral")

    # 2. Standardize Confidence
    if "confidence" not in df.columns:
        df["confidence"] = 0.78
    else:
        df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce").fillna(0.75).clip(0.0, 1.0)

    # 3. Clean Text
    if "clean_text" not in df.columns:
        if "cleaned_text" in df.columns:
            df["clean_text"] = df["cleaned_text"]
        elif "text" in df.columns:
            df["clean_text"] = df["text"]
        else:
            df["clean_text"] = ""

    df["clean_text"] = df["clean_text"].fillna("").astype(str)

    # 4. Standardize Topic & Aspect
    if "topic" not in df.columns:
        df["topic"] = "general_reading"
    if "aspect" not in df.columns:
        df["aspect"] = "general feedback"

    # 5. Business Dimensions (Seed for consistency)
    n = len(df)
    if n > 0:
        rng = np.random.default_rng(42)

        if "sales" not in df.columns:
            df["sales"] = rng.integers(250, 4800, size=n)

        if "region" not in df.columns:
            df["region"] = rng.choice(["North", "South", "East", "West"], size=n)

        if "store" not in df.columns:
            df["store"] = rng.choice(["Downtown Plaza", "Metropolis Mall", "Tech Hub", "Airport Terminal", "Suburban Center"], size=n)

        if "category" not in df.columns:
            df["category"] = rng.choice(["Technology & AI", "Business & Finance", "Fiction & Mystery", "Self-Help & Habits", "Science & Society"], size=n)

        if "date" not in df.columns:
            days_ago = rng.integers(0, 90, size=n)
            df["date"] = pd.to_datetime("today") - pd.to_timedelta(days_ago, unit="D")

    return df


# Backwards compatibility alias
load_sentiment_data = load_book_data
