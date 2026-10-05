"""
Legacy validation entrypoint.
Delegates to book_market_intelligence.preprocessing.validator.validate_feedback_dataframe.
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.preprocessing.validator import validate_feedback_dataframe
from book_market_intelligence.config.settings import settings


def main():
    target_path = settings.processed_cleaned_text_path
    if not target_path.exists():
        print(f"✗ File {target_path} not found.")
        return

    df = pd.read_csv(target_path)
    validated_df, stats = validate_feedback_dataframe(df)

    print("\n" + "=" * 50)
    print("DATASET VALIDATION REPORT")
    print("=" * 50)
    for k, v in stats.items():
        print(f"{k:25}: {v}")
    print("=" * 50)

    # Persist validated output
    output_path = settings.PROCESSED_DATA_DIR / "validated_cleaned_text.csv"
    validated_df.to_csv(output_path, index=False)
    print(f"✓ Validated dataset saved to: {output_path}")


if __name__ == "__main__":
    main()