"""
Batch Sentiment Analysis runner.
Uses enterprise SentimentAnalyzer with batch processing and progress monitoring.
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.analytics.sentiment import sentiment_analyzer
from book_market_intelligence.config.settings import settings


def run_batch_sentiment(batch_size: int = 50):
    input_file = settings.processed_cleaned_text_path
    output_file = settings.processed_sentiment_results_path

    if not input_file.exists():
        print(f"✗ Error: Input file '{input_file}' not found.")
        return

    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} records from {input_file}")
    print(f"Processing in batches of {batch_size}...")

    texts = df["clean_text"].astype(str).tolist()
    sentiments, confidences = sentiment_analyzer.analyze_batch(texts)

    df["sentiment"] = sentiments
    df["confidence"] = confidences

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✓ Results saved to {output_file}")


if __name__ == "__main__":
    run_batch_sentiment()
