"""
Legacy text preprocessing script.
Delegates to book_market_intelligence.preprocessing.pipeline.run_preprocessing_pipeline.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.preprocessing.pipeline import run_preprocessing_pipeline


def main():
    print("▶ Executing data cleaning and normalization pipeline...")
    df = run_preprocessing_pipeline()
    print(f"✅ Preprocessing completed. {len(df)} cleaned records saved.")


if __name__ == "__main__":
    main()
