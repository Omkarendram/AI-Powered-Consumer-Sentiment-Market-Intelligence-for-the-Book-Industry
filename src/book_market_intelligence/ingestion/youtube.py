"""
YouTube Data API v3 collector for book reviews and community feedback.
"""

from typing import Optional, List, Dict
import time
import pandas as pd
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger
from book_market_intelligence.ingestion.base import BaseCollector


class YouTubeCollector(BaseCollector):
    """Collects comments from book review videos using YouTube Data API v3."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        super().__init__(name="YouTubeCollector")
        self.api_key = api_key or settings.YOUTUBE_API_KEY

    def collect(
        self,
        query: str = "book review",
        max_videos: int = 15,
        comments_per_video: int = 50
    ) -> pd.DataFrame:
        if not self.api_key:
            logger.warning("YOUTUBE_API_KEY is not set. Skipping live YouTube ingestion.")
            return pd.DataFrame()

        try:
            from googleapiclient.discovery import build
            youtube = build("youtube", "v3", developerKey=self.api_key)
        except ImportError:
            logger.error("google-api-python-client is not installed. Run `pip install google-api-python-client`.")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Failed to initialize YouTube service: {e}")
            return pd.DataFrame()

        logger.info(f"Searching YouTube videos for '{query}'...")
        comments_data: List[Dict] = []

        try:
            search_request = youtube.search().list(
                q=query,
                part="snippet",
                type="video",
                maxResults=max_videos
            )
            search_response = search_request.execute()
            video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
        except Exception as e:
            logger.error(f"YouTube search request failed: {e}")
            return pd.DataFrame()

        for idx, video_id in enumerate(video_ids, start=1):
            try:
                video_res = youtube.videos().list(part="snippet", id=video_id).execute()
                items = video_res.get("items", [])
                video_title = items[0]["snippet"]["title"] if items else "Unknown Video"
            except Exception:
                video_title = "Unknown Video"

            next_page_token = None
            collected = 0

            while collected < comments_per_video:
                try:
                    comment_request = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        maxResults=min(100, comments_per_video - collected),
                        pageToken=next_page_token,
                        textFormat="plainText"
                    )
                    comment_response = comment_request.execute()
                except Exception as e:
                    logger.warning(f"Could not fetch comments for video {video_id}: {e}")
                    break

                for item in comment_response.get("items", []):
                    snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
                    comments_data.append({
                        "video_title": video_title,
                        "comment_text": snippet.get("textDisplay", ""),
                        "author": snippet.get("authorDisplayName", ""),
                        "like_count": snippet.get("likeCount", 0),
                        "published_at": snippet.get("publishedAt", ""),
                        "source": "youtube"
                    })
                    collected += 1

                next_page_token = comment_response.get("nextPageToken")
                if not next_page_token:
                    break

                time.sleep(0.2)

        df = pd.DataFrame(comments_data)
        logger.info(f"Collected {len(df)} total comments from YouTube.")
        return df
