"""
Sentiment Analysis runner.
Uses enterprise SentimentAnalyzer with Groq LLM integration and deterministic fallback.
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.analytics.sentiment import sentiment_analyzer
from book_market_intelligence.config.settings import settings


def run_sentiment_analysis(limit: int = None):
    input_file = settings.processed_cleaned_text_path
    output_file = settings.PROCESSED_DATA_DIR / "sentiment_analysis_results.csv"

    if not input_file.exists():
        print(f"✗ Error: Input file '{input_file}' not found.")
        return

    df = pd.read_csv(input_file)
    if limit:
        df = df.head(limit)

    print(f"\nLoaded {len(df)} records from {input_file}")
    print("Starting sentiment analysis...")

    texts = df["clean_text"].astype(str).tolist()
    sentiments, confidences = sentiment_analyzer.analyze_batch(texts)

    df["sentiment"] = sentiments
    df["confidence"] = confidences

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)

    print(f"\n✓ Sentiment analysis complete! Results saved to {output_file}")
    print("\nSentiment Summary:")
    print(df["sentiment"].value_counts())
    print(f"Average Confidence: {df['confidence'].mean():.2f}")


if __name__ == "__main__":
    run_sentiment_analysis()
