"""
Aspect extraction and topic modeling engine for book market intelligence.
"""

import json
import re
import time
from typing import Tuple, Optional, Dict, List
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger

VALID_TOPICS = [
    "platform_experience",
    "story_quality",
    "pricing",
    "delivery",
    "author_opinion",
    "genre_preference",
    "general_reading"
]

TOPIC_KEYWORDS = {
    "platform_experience": ["app", "website", "kindle", "audiobook", "download", "ui", "login", "crash", "platform", "interface"],
    "story_quality": ["plot", "character", "story", "ending", "writing", "twist", "pacing", "boring", "engaging", "climax"],
    "pricing": ["price", "cost", "expensive", "cheap", "worth", "discount", "offer", "rupees", "dollar", "money", "afford"],
    "delivery": ["delivery", "shipping", "courier", "package", "delay", "damaged", "binding", "page quality", "paper", "cover"],
    "author_opinion": ["author", "writer", "style", "chetan", "colleen", "rowling", "harari", "voice", "perspective"],
    "genre_preference": ["fiction", "non-fiction", "fantasy", "thriller", "self-help", "sci-fi", "romance", "mythology", "history"],
    "general_reading": ["book", "reading", "read", "recommend", "habit", "time", "library", "collection"]
}


class TopicExtractor:
    """Extracts thematic topic and specific aspect phrases from reader feedback."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = settings.GROQ_FALLBACK_MODEL
        self._groq_client = None

        if self.api_key:
            try:
                from groq import Groq
                self._groq_client = Groq(api_key=self.api_key)
            except Exception:
                pass

    def _fallback_topic(self, text: str) -> Tuple[str, str]:
        """Keyword-based deterministic topic and aspect extractor."""
        lower = text.lower()

        matched_topic = "general_reading"
        max_matches = 0

        for topic, keywords in TOPIC_KEYWORDS.items():
            matches = sum(1 for kw in keywords if re.search(r"\b" + re.escape(kw) + r"\b", lower))
            if matches > max_matches:
                max_matches = matches
                matched_topic = topic

        # Simple aspect derivation
        aspect = "general appreciation"
        if matched_topic == "pricing":
            aspect = "high price" if "expensive" in lower else "affordable pricing"
        elif matched_topic == "delivery":
            aspect = "damaged page" if "damaged" in lower or "binding" in lower else "delivery speed"
        elif matched_topic == "story_quality":
            aspect = "weak plot" if "boring" in lower or "slow" in lower else "compelling narrative"
        elif matched_topic == "platform_experience":
            aspect = "app stability" if "crash" in lower else "user interface"

        return matched_topic, aspect

    def extract(self, text: str, max_retries: int = 1) -> Tuple[str, str]:
        """
        Classifies topic and extracts aspect from text.
        Returns: (topic: str, aspect: str)
        """
        if not text or not str(text).strip():
            return "general_reading", "unspecified"

        if not self._groq_client:
            return self._fallback_topic(text)

        prompt = f"""Classify this book customer feedback:
Topic (choose one): platform_experience, story_quality, pricing, delivery, author_opinion, genre_preference, general_reading
Aspect: short phrase describing exact issue or praise (max 4 words)

Respond ONLY in JSON format:
{{"topic": "delivery", "aspect": "damaged binding"}}

Feedback: {text[:400]}"""

        for attempt in range(max_retries + 1):
            try:
                res = self._groq_client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=60
                )
                raw = res.choices[0].message.content.strip()
                match = re.search(r"\{.*?\}", raw, re.DOTALL)
                if match:
                    parsed = json.loads(match.group(0))
                    topic = parsed.get("topic", "general_reading")
                    aspect = parsed.get("aspect", "unspecified")
                    if topic not in VALID_TOPICS:
                        topic = "general_reading"
                    return topic, aspect[:40]
            except Exception:
                if attempt < max_retries:
                    time.sleep(1.0)
                    continue
                break

        return self._fallback_topic(text)


topic_extractor = TopicExtractor()
