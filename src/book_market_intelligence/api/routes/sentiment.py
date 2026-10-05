"""
Sentiment analysis inference routes.
"""

from fastapi import APIRouter
from book_market_intelligence.api.schemas import (
    SentimentRequest,
    SentimentResponse,
    BatchSentimentRequest,
    BatchSentimentResponse
)
from book_market_intelligence.analytics.sentiment import sentiment_analyzer

router = APIRouter(prefix="/api/v1/sentiment", tags=["Sentiment"])


@router.post("/predict", response_model=SentimentResponse)
def predict_sentiment(req: SentimentRequest) -> SentimentResponse:
    """Predicts sentiment category (positive, negative, neutral) and confidence score."""
    sentiment, confidence = sentiment_analyzer.analyze(req.text)
    return SentimentResponse(
        text=req.text,
        sentiment=sentiment,
        confidence=confidence
    )


@router.post("/batch", response_model=BatchSentimentResponse)
def batch_predict_sentiment(req: BatchSentimentRequest) -> BatchSentimentResponse:
    """Performs batch sentiment scoring across multiple consumer feedback texts."""
    sentiments, confidences = sentiment_analyzer.analyze_batch(req.texts)
    results = [
        SentimentResponse(text=t, sentiment=s, confidence=c)
        for t, s, c in zip(req.texts, sentiments, confidences)
    ]
    return BatchSentimentResponse(total=len(results), results=results)
