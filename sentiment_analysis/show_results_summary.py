"""
Sentiment summary statistics viewer.
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.config.settings import settings


def main():
    target = settings.processed_sentiment_results_path
    if not target.exists():
        target = settings.PROCESSED_DATA_DIR / "sentiment_analysis_results.csv"

    if not target.exists():
        print(f"✗ No sentiment results found at {target}.")
        return

    df = pd.read_csv(target)
    print("=" * 60)
    print("SENTIMENT ANALYSIS RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total Records Analyzed: {len(df)}")

    if "sentiment" in df.columns:
        print("\n--- SENTIMENT DISTRIBUTION ---")
        counts = df["sentiment"].astype(str).str.lower().value_counts()
        for sent in ["positive", "negative", "neutral"]:
            count = counts.get(sent, 0)
            pct = (count / len(df) * 100) if len(df) > 0 else 0
            print(f"  {sent.upper():10} : {count:4d} ({pct:6.2f}%)")

    if "confidence" in df.columns:
        conf = pd.to_numeric(df["confidence"], errors="coerce").dropna()
        print("\n--- CONFIDENCE METRICS ---")
        print(f"  Mean     : {conf.mean():.2f}")
        print(f"  Median   : {conf.median():.2f}")
        print(f"  Min      : {conf.min():.2f}")
        print(f"  Max      : {conf.max():.2f}")

    print("=" * 60)


if __name__ == "__main__":
    main()
