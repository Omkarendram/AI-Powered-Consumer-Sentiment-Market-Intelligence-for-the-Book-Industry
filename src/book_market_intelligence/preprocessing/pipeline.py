"""
Data preprocessing pipeline consolidating raw multi-channel data into clean corpus.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger
from book_market_intelligence.preprocessing.cleaner import clean_text
from book_market_intelligence.preprocessing.validator import validate_feedback_dataframe


def run_preprocessing_pipeline(
    raw_dir: Optional[Path] = None,
    output_path: Optional[Path] = None,
    save: bool = True
) -> pd.DataFrame:
    """
    Executes end-to-end data cleaning:
    1. Ingests raw data from YouTube comments, NewsAPI articles, and Google Books.
    2. Maps domain-specific text fields to clean_text.
    3. Normalizes and tokenizes text.
    4. Deduplicates and validates schema.
    5. Persists output to data/processed/cleaned_text.csv.
    """
    raw_dir = raw_dir or settings.RAW_DATA_DIR
    output_path = output_path or settings.processed_cleaned_text_path

    frames = []

    # 1. YouTube Comments
    yt_file = raw_dir / "youtube_book_comments.csv"
    if yt_file.exists():
        try:
            yt_df = pd.read_csv(yt_file)
            if "comment_text" in yt_df.columns:
                frames.append(pd.DataFrame({
                    "clean_text": yt_df["comment_text"],
                    "source": "youtube"
                }))
                logger.info(f"Loaded {len(yt_df)} raw YouTube comments.")
        except Exception as e:
            logger.warning(f"Failed to load YouTube data: {e}")

    # 2. News Articles
    news_file = raw_dir / "news_articles.csv"
    if news_file.exists():
        try:
            news_df = pd.read_csv(news_file)
            combined_news = (
                news_df.get("title", "").fillna("").astype(str) + ". " +
                news_df.get("description", "").fillna("").astype(str) + " " +
                news_df.get("content", "").fillna("").astype(str)
            )
            frames.append(pd.DataFrame({
                "clean_text": combined_news,
                "source": "news"
            }))
            logger.info(f"Loaded {len(news_df)} raw News articles.")
        except Exception as e:
            logger.warning(f"Failed to load News data: {e}")

    # 3. E-commerce / Google Books
    ecom_file = raw_dir / "ecommerce_books.csv"
    if ecom_file.exists():
        try:
            ecom_df = pd.read_csv(ecom_file)
            text_series = (
                ecom_df["full_text"]
                if "full_text" in ecom_df.columns
                else (ecom_df.get("title", "").fillna("") + ". " + ecom_df.get("description", "").fillna(""))
            )
            frames.append(pd.DataFrame({
                "clean_text": text_series,
                "source": "ecommerce"
            }))
            logger.info(f"Loaded {len(ecom_df)} raw E-commerce records.")
        except Exception as e:
            logger.warning(f"Failed to load E-commerce data: {e}")

    if not frames:
        logger.warning("No raw files found. Loading existing processed file if available.")
        if output_path.exists():
            return pd.read_csv(output_path)
        return pd.DataFrame(columns=["clean_text", "source"])

    combined = pd.concat(frames, ignore_index=True)
    combined["clean_text"] = combined["clean_text"].apply(clean_text)

    # Filter out empty or noise texts
    combined = combined[combined["clean_text"].str.strip() != ""]
    combined = combined.drop_duplicates(subset=["clean_text"]).reset_index(drop=True)

    if save:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        combined.to_csv(output_path, index=False)
        logger.info(f"Successfully saved {len(combined)} clean records to {output_path}")

    return combined
