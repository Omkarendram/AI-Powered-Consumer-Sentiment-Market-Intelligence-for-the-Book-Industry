"""
Business intelligence and analytics reporting routes.
"""

from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from fastapi import APIRouter
from book_market_intelligence.api.schemas import AnalyticsOverviewResponse
from book_market_intelligence.analytics.metrics import calculate_kpis, get_topic_breakdown, get_top_aspects
from book_market_intelligence.config.settings import settings

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


def _load_active_data() -> pd.DataFrame:
    for path in [
        settings.processed_topics_path,
        settings.processed_feedback_path,
        settings.processed_sentiment_results_path
    ]:
        if path.exists():
            return pd.read_csv(path)
    return pd.DataFrame()


@router.get("/overview", response_model=AnalyticsOverviewResponse)
def get_analytics_overview() -> AnalyticsOverviewResponse:
    """Returns high-level business intelligence metrics and sentiment ratios."""
    df = _load_active_data()
    kpis = calculate_kpis(df)
    return AnalyticsOverviewResponse(**kpis)


@router.get("/topics")
def get_topics_analytics() -> List[Dict[str, Any]]:
    """Returns top customer topics with volume and negative feedback percentages."""
    df = _load_active_data()
    topics_df = get_topic_breakdown(df, top_n=10)
    return topics_df.to_dict(orient="records")


@router.get("/aspects")
def get_aspects_analytics(sentiment: str = "negative") -> List[Dict[str, Any]]:
    """Returns top complaint or praise aspects filtered by sentiment."""
    df = _load_active_data()
    aspects_df = get_top_aspects(df, sentiment_filter=sentiment, top_n=10)
    return aspects_df.to_dict(orient="records")
