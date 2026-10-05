"""
Enterprise sentiment analysis engine supporting Groq LLM inference and offline fallback.
"""

import json
import os
import re
import time
from typing import Tuple, List, Optional, Dict, Any
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger

POSITIVE_LEXICON = {
    "great", "excellent", "love", "amazing", "good", "best", "recommend",
    "inspiring", "helpful", "masterpiece", "informative", "enjoyed", "fantastic",
    "brilliant", "awesome", "perfect", "worth", "favorite", "favourite", "superb",
    "wonderful", "valuable", "gem", "classic", "clean", "easy", "liked", "nice"
}

NEGATIVE_LEXICON = {
    "bad", "terrible", "worst", "boring", "waste", "disappointed", "poor",
    "hate", "awful", "horrible", "damaged", "regret", "useless", "broken",
    "crash", "crashes", "overhyped", "repetitive", "slow", "annoying", "cheap",
    "torn", "fake", "confusing", "misleading", "dull", "garbage", "trash"
}


class SentimentAnalyzer:
    """
    Production sentiment analysis engine:
    1. Uses Groq LLM (LLaMA 3.3 70B / 3.1 8B) when API key is available.
    2. Gracefully falls back to high-precision rule-based sentiment classifier when offline.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None) -> None:
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_FALLBACK_MODEL
        self._groq_client = None

        if self.api_key:
            try:
                from groq import Groq
                self._groq_client = Groq(api_key=self.api_key)
                logger.info(f"Initialized Groq SentimentAnalyzer with model '{self.model}'.")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq client: {e}. Fallback enabled.")

    def _fallback_sentiment(self, text: str) -> Tuple[str, float]:
        """High-precision heuristic sentiment classifier for offline or rate-limited scenarios."""
        tokens = set(re.findall(r"\b[a-z]{3,}\b", text.lower()))
        pos_matches = len(tokens.intersection(POSITIVE_LEXICON))
        neg_matches = len(tokens.intersection(NEGATIVE_LEXICON))

        # Check for negations
        has_negation = bool(re.search(r"\b(not|never|no|hardly|scarcely)\b\s+\b[a-z]+\b", text.lower()))

        if pos_matches > neg_matches:
            if has_negation:
                return "neutral", 0.65
            conf = min(0.70 + (pos_matches * 0.08), 0.95)
            return "positive", round(conf, 2)
        elif neg_matches > pos_matches:
            conf = min(0.72 + (neg_matches * 0.08), 0.95)
            return "negative", round(conf, 2)
        else:
            return "neutral", 0.60

    def analyze(self, text: str, max_retries: int = 2) -> Tuple[str, float]:
        """
        Analyzes sentiment of given text.
        Returns: (sentiment: 'positive'|'negative'|'neutral', confidence: float)
        """
        if not text or not str(text).strip():
            return "neutral", 0.0

        clean_input = str(text).strip()

        # If Groq is not configured, use fallback immediately
        if not self._groq_client:
            return self._fallback_sentiment(clean_input)

        prompt = f"""Respond with ONLY a JSON object in this exact format:
{{"sentiment": "positive|negative|neutral", "confidence": 0.0-1.0}}

Customer text: {clean_input[:500]}"""

        for attempt in range(max_retries + 1):
            try:
                response = self._groq_client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                    max_tokens=40
                )
                raw_out = response.choices[0].message.content.strip()

                # Extract JSON bracket match
                match = re.search(r"\{.*?\}", raw_out, re.DOTALL)
                if match:
                    parsed = json.loads(match.group(0))
                    sentiment = str(parsed.get("sentiment", "neutral")).lower().strip()
                    confidence = float(parsed.get("confidence", 0.7))

                    if sentiment not in ["positive", "negative", "neutral"]:
                        sentiment = "neutral"

                    confidence = max(0.0, min(1.0, confidence))
                    return sentiment, round(confidence, 2)

            except Exception as e:
                if "429" in str(e) and attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue
                logger.debug(f"Groq API sentiment attempt failed: {e}. Using fallback.")
                break

        return self._fallback_sentiment(clean_input)

    def analyze_batch(
        self,
        texts: List[str],
        batch_delay: float = 0.2
    ) -> Tuple[List[str], List[float]]:
        """Analyzes a sequence of texts with polite rate limiting."""
        sentiments: List[str] = []
        confidences: List[float] = []

        for t in texts:
            s, c = self.analyze(t)
            sentiments.append(s)
            confidences.append(c)
            if self._groq_client and batch_delay > 0:
                time.sleep(batch_delay)

        return sentiments, confidences


# Singleton analyzer instance
sentiment_analyzer = SentimentAnalyzer()
