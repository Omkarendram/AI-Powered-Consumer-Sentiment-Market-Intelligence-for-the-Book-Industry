"""
NewsAPI data collector for book industry articles and publishing trends.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict
import time
import requests
import pandas as pd
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger
from book_market_intelligence.core.exceptions import DataIngestionError
from book_market_intelligence.ingestion.base import BaseCollector

DEFAULT_QUERY = "(books OR publishing OR ebook OR reading OR book sales OR author OR bookstore)"
BASE_URL = "https://newsapi.org/v2/everything"


class NewsCollector(BaseCollector):
    """Fetches articles using NewsAPI v2 with windowed dates and rate-limiting."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        super().__init__(name="NewsCollector")
        self.api_key = api_key or settings.NEWS_API_KEY

    def collect(self, limit: int = 100, days_back: int = 30) -> pd.DataFrame:
        if not self.api_key:
            logger.warning("NEWS_API_KEY is not set. Skipping live news ingestion.")
            return pd.DataFrame()

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days_back)
        articles: List[Dict] = []
        current_start = start_date

        logger.info(f"Collecting news articles from {start_date.date()} to {end_date.date()}...")

        while current_start < end_date and len(articles) < limit:
            current_end = min(current_start + timedelta(days=5), end_date)
            page = 1

            while len(articles) < limit:
                params = {
                    "q": DEFAULT_QUERY,
                    "language": "en",
                    "pageSize": min(100, limit - len(articles)),
                    "page": page,
                    "from": current_start.strftime("%Y-%m-%d"),
                    "to": current_end.strftime("%Y-%m-%d"),
                    "apiKey": self.api_key,
                    "sortBy": "publishedAt"
                }

                try:
                    res = requests.get(BASE_URL, params=params, timeout=15)
                except Exception as e:
                    logger.error(f"NewsAPI connection failed: {e}")
                    break

                if res.status_code != 200:
                    logger.warning(f"NewsAPI returned status {res.status_code}: {res.text[:100]}")
                    break

                data = res.json()
                fetched = data.get("articles", [])
                if not fetched:
                    break

                for item in fetched:
                    articles.append({
                        "title": item.get("title", ""),
                        "description": item.get("description", ""),
                        "content": item.get("content", ""),
                        "source": item.get("source", {}).get("name", "news"),
                        "published_at": item.get("publishedAt", ""),
                        "category": "ecommerce_news"
                    })
                    if len(articles) >= limit:
                        break

                page += 1
                time.sleep(1)

            current_start = current_end

        df = pd.DataFrame(articles).drop_duplicates(subset=["title", "content"])
        logger.info(f"Finished collecting {len(df)} news articles.")
        return df
