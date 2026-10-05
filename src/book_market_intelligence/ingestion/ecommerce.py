"""
Google Books API / E-commerce proxy collector with retry logic.
"""

from typing import List, Dict, Set
import time
import requests
import pandas as pd
from book_market_intelligence.core.logging import logger
from book_market_intelligence.ingestion.base import BaseCollector

API_URL = "https://www.googleapis.com/books/v1/volumes"
DEFAULT_QUERY = "books subject:technology OR programming OR software OR AI OR data science"


class EcommerceCollector(BaseCollector):
    """Fetches book metadata, descriptions, and ratings via Google Books API."""

    def __init__(self) -> None:
        super().__init__(name="EcommerceCollector")

    def collect(self, query: str = DEFAULT_QUERY, target_count: int = 100) -> pd.DataFrame:
        books: List[Dict] = []
        start_index = 0
        max_per_call = 40
        seen_ids: Set[str] = set()
        retries = 0
        max_retries = 3

        logger.info(f"Starting Google Books collection for query: '{query}'...")

        while len(books) < target_count:
            params = {
                "q": query,
                "startIndex": start_index,
                "maxResults": max_per_call,
                "printType": "books",
                "langRestrict": "en"
            }

            try:
                response = requests.get(API_URL, params=params, timeout=15)
            except Exception as e:
                logger.error(f"Google Books API request failed: {e}")
                break

            if response.status_code == 429:
                retries += 1
                if retries >= max_retries:
                    logger.warning("Reached rate limit cap (429) for Google Books API.")
                    break
                time.sleep(2 ** retries)
                continue

            if response.status_code != 200:
                logger.warning(f"Google Books API returned status {response.status_code}.")
                break

            retries = 0
            data = response.json()
            items = data.get("items", [])
            if not items:
                break

            for item in items:
                volume = item.get("volumeInfo", {})
                book_id = item.get("id")
                if not book_id or book_id in seen_ids:
                    continue
                seen_ids.add(book_id)

                title = volume.get("title", "") or ""
                description = volume.get("description", "") or ""
                full_text = f"{title}. {description}".strip()

                if not full_text:
                    continue

                books.append({
                    "title": title,
                    "authors": ", ".join(volume.get("authors", [])),
                    "description": description,
                    "full_text": full_text,
                    "average_rating": volume.get("averageRating", None),
                    "categories": ", ".join(volume.get("categories", [])),
                    "published_date": volume.get("publishedDate", ""),
                    "source": "google_books_api"
                })

                if len(books) >= target_count:
                    break

            start_index += max_per_call
            time.sleep(0.5)

        df = pd.DataFrame(books).drop_duplicates(subset=["title", "description"])
        logger.info(f"Collected {len(df)} e-commerce book records.")
        return df
