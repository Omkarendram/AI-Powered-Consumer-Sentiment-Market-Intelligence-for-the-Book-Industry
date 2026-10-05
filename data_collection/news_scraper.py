"""
Legacy entrypoint for News article collection.
Delegates to book_market_intelligence.ingestion.news.NewsCollector.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.ingestion.news import NewsCollector
from book_market_intelligence.config.settings import settings


def main():
    collector = NewsCollector()
    df = collector.collect(limit=100)
    if not df.empty:
        collector.save(df, settings.raw_news_path)
    else:
        print("No articles collected. Ensure NEWS_API_KEY is configured in .env.")


if __name__ == "__main__":
    main()