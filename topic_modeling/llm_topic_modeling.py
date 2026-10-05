"""
Topic modeling runner using LLM and keyword cluster extraction.
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.analytics.topics import topic_extractor
from book_market_intelligence.config.settings import settings


def main(limit: int = 100):
    input_file = settings.processed_cleaned_text_path
    output_file = settings.PROCESSED_DATA_DIR / "llm_topic_results.csv"

    if not input_file.exists():
        print(f"✗ Input file '{input_file}' not found.")
        return

    df = pd.read_csv(input_file).head(limit)
    print(f"▶ Running topic clustering across {len(df)} records...")

    results = []
    for idx, text in enumerate(df["clean_text"]):
        topic, aspect = topic_extractor.extract(str(text))
        results.append({
            "record_id": idx,
            "text": str(text)[:80],
            "topic": topic,
            "aspect": aspect
        })

    out_df = pd.DataFrame(results)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(output_file, index=False)
    print(f"✓ Saved topic modeling results to: {output_file}")


if __name__ == "__main__":
    main()