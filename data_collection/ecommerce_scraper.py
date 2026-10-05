"""
Legacy entrypoint for Google Books e-commerce data collection.
Delegates to book_market_intelligence.ingestion.ecommerce.EcommerceCollector.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.ingestion.ecommerce import EcommerceCollector
from book_market_intelligence.config.settings import settings


def main():
    collector = EcommerceCollector()
    df = collector.collect(target_count=100)
    if not df.empty:
        collector.save(df, settings.raw_ecommerce_path)


if __name__ == "__main__":
    main()
