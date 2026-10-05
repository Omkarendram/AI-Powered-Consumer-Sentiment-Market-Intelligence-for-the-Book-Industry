"""
Unit tests for sentiment analysis and aspect classification.
"""

from book_market_intelligence.analytics.sentiment import SentimentAnalyzer
from book_market_intelligence.analytics.topics import TopicExtractor


def test_sentiment_analyzer_positive():
    analyzer = SentimentAnalyzer()
    sentiment, confidence = analyzer.analyze("This book is an absolute masterpiece! Highly recommend reading it.")
    assert sentiment == "positive"
    assert 0.5 <= confidence <= 1.0


def test_sentiment_analyzer_negative():
    analyzer = SentimentAnalyzer()
    sentiment, confidence = analyzer.analyze("The book arrived damaged with terrible binding, completely useless waste.")
    assert sentiment == "negative"
    assert 0.5 <= confidence <= 1.0


def test_sentiment_analyzer_empty():
    analyzer = SentimentAnalyzer()
    sentiment, confidence = analyzer.analyze("")
    assert sentiment == "neutral"
    assert confidence == 0.0


def test_topic_extractor_pricing():
    extractor = TopicExtractor()
    topic, aspect = extractor.extract("The book price is way too expensive for what it offers.")
    assert topic == "pricing"
    assert aspect != ""


def test_topic_extractor_delivery():
    extractor = TopicExtractor()
    topic, aspect = extractor.extract("Courier took two weeks and the book package was badly damaged.")
    assert topic == "delivery"
    assert aspect != ""
