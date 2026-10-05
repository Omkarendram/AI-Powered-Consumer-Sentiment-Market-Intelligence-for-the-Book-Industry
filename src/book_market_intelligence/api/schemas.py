"""
Pydantic schemas for the FastAPI backend.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "2.0.0"
    environment: str = "production"
    service: str = "book-market-intelligence-api"


class SentimentRequest(BaseModel):
    text: str = Field(..., description="Review or customer comment to analyze", min_length=1)


class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    confidence: float


class BatchSentimentRequest(BaseModel):
    texts: List[str] = Field(..., description="List of comments for batch analysis")


class BatchSentimentResponse(BaseModel):
    total: int
    results: List[SentimentResponse]


class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="Business question for the market intelligence RAG system")
    top_k: Optional[int] = Field(default=5, ge=1, le=20)


class RAGQueryResponse(BaseModel):
    query: str
    answer: str
    query_type: str
    retrieved_documents: List[Dict[str, Any]]


class AnalyticsOverviewResponse(BaseModel):
    total_feedback: int
    positive_count: int
    negative_count: int
    neutral_count: int
    positive_rate: float
    negative_rate: float
    neutral_rate: float
    average_confidence: float
    risk_ratio: float
    risk_level: str
