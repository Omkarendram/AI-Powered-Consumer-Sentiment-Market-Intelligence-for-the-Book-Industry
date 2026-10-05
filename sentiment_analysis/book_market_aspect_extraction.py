"""
Aspect Extraction and Topic Classification.
Uses enterprise TopicExtractor and SentimentAnalyzer.
"""

import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.analytics.topics import topic_extractor
from book_market_intelligence.analytics.sentiment import sentiment_analyzer
from book_market_intelligence.config.settings import settings


def run_aspect_extraction(limit: int = None):
    input_file = settings.processed_cleaned_text_path
    output_file = settings.processed_topics_path

    if not input_file.exists():
        print(f"✗ Input file '{input_file}' not found.")
        return

    df = pd.read_csv(input_file)
    if limit:
        df = df.head(limit)

    print(f"Extracting topics and aspects across {len(df)} feedback records...")

    topics, aspects, sentiments = [], [], []

    for text in df["clean_text"]:
        t, a = topic_extractor.extract(str(text))
        s, _ = sentiment_analyzer.analyze(str(text))
        topics.append(t)
        aspects.append(a)
        sentiments.append(s)

    df["sentiment"] = sentiments
    df["topic"] = topics
    df["aspect"] = aspects

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✓ Aspect extraction completed! Saved to {output_file}")


if __name__ == "__main__":
    run_aspect_extraction()
