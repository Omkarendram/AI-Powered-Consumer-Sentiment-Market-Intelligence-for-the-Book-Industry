"""
Consolidates sentiment-annotated records into unified book_feedback.csv.
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.config.settings import settings
from book_market_intelligence.preprocessing.validator import validate_feedback_dataframe


def main():
    candidate_files = [
        settings.PROCESSED_DATA_DIR / "book_market_sentiment_topics.csv",
        settings.PROCESSED_DATA_DIR / "sentiment_analysis_results_batch.csv",
        settings.PROCESSED_DATA_DIR / "sentiment_analysis_results.csv",
    ]

    dfs = []
    for f in candidate_files:
        if f.exists():
            try:
                df = pd.read_csv(f)
                df.columns = [c.strip().lower() for c in df.columns]
                if "clean_text" in df.columns and "sentiment" in df.columns:
                    dfs.append(df)
                    print(f"Loaded {f.name} with {len(df)} rows")
            except Exception as e:
                print(f"Skipping {f.name}: {e}")

    if not dfs:
        print("✗ No sentiment datasets available to merge.")
        return

    merged = pd.concat(dfs, ignore_index=True)
    validated_df, stats = validate_feedback_dataframe(merged)

    output_path = settings.processed_feedback_path
    validated_df.to_csv(output_path, index=False)
    print(f"\n✓ Successfully created {output_path} with {len(validated_df)} unified records.")


if __name__ == "__main__":
    main()
