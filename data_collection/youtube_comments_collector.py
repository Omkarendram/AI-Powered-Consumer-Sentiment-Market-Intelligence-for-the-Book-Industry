"""
Legacy entrypoint for YouTube comments collection.
Delegates to book_market_intelligence.ingestion.youtube.YouTubeCollector.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.ingestion.youtube import YouTubeCollector
from book_market_intelligence.config.settings import settings


def main():
    collector = YouTubeCollector()
    df = collector.collect(query="book review", max_videos=10, comments_per_video=50)
    if not df.empty:
        collector.save(df, settings.raw_youtube_path)
    else:
        print("No YouTube comments collected. Ensure YOUTUBE_API_KEY is configured in .env.")


if __name__ == "__main__":
    main()