"""
Business analytics, KPI calculations, and risk metric aggregation.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np


def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes key performance indicators across consumer feedback data.
    """
    if df is None or df.empty:
        return {
            "total_feedback": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "positive_rate": 0.0,
            "negative_rate": 0.0,
            "neutral_rate": 0.0,
            "average_confidence": 0.0,
            "risk_ratio": 0.0,
            "risk_level": "STABLE"
        }

    sentiment_col = None
    for c in df.columns:
        if "sentiment" in c.lower():
            sentiment_col = c
            break

    if not sentiment_col:
        sentiment_series = pd.Series(["Neutral"] * len(df))
    else:
        sentiment_series = df[sentiment_col].astype(str).str.title()

    total = len(df)
    pos_count = int((sentiment_series == "Positive").sum())
    neg_count = int((sentiment_series == "Negative").sum())
    neu_count = int((sentiment_series == "Neutral").sum())

    pos_rate = round((pos_count / total) * 100, 2) if total > 0 else 0.0
    neg_rate = round((neg_count / total) * 100, 2) if total > 0 else 0.0
    neu_rate = round((neu_count / total) * 100, 2) if total > 0 else 0.0
    risk_ratio = round(neg_count / total, 4) if total > 0 else 0.0

    if risk_ratio >= 0.35:
        risk_level = "CRITICAL"
    elif risk_ratio >= 0.20:
        risk_level = "ELEVATED"
    elif risk_ratio >= 0.10:
        risk_level = "MODERATE"
    else:
        risk_level = "HEALTHY"

    conf_col = "confidence" if "confidence" in df.columns else None
    if conf_col:
        avg_conf = round(float(pd.to_numeric(df[conf_col], errors="coerce").fillna(0).mean()), 2)
    else:
        avg_conf = 0.75

    return {
        "total_feedback": total,
        "positive_count": pos_count,
        "negative_count": neg_count,
        "neutral_count": neu_count,
        "positive_rate": pos_rate,
        "negative_rate": neg_rate,
        "neutral_rate": neu_rate,
        "average_confidence": avg_conf,
        "risk_ratio": risk_ratio,
        "risk_level": risk_level
    }


def get_topic_breakdown(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Returns top customer feedback topics with sentiment splits."""
    if df is None or df.empty or "topic" not in df.columns:
        return pd.DataFrame(columns=["topic", "count", "negative_rate"])

    grouped = df.groupby("topic").agg(
        total_count=("topic", "count"),
        negative_count=("sentiment", lambda s: (s.astype(str).str.lower() == "negative").sum())
    ).reset_index()

    grouped["negative_rate"] = round((grouped["negative_count"] / grouped["total_count"]) * 100, 1)
    grouped = grouped.sort_values("total_count", ascending=False).head(top_n)
    return grouped


def get_top_aspects(df: pd.DataFrame, sentiment_filter: Optional[str] = None, top_n: int = 10) -> pd.DataFrame:
    """Extracts top specific aspects/praise/complaint phrases."""
    if df is None or df.empty or "aspect" not in df.columns:
        return pd.DataFrame(columns=["aspect", "count"])

    sub_df = df
    if sentiment_filter and "sentiment" in df.columns:
        sub_df = df[df["sentiment"].astype(str).str.lower() == sentiment_filter.lower()]

    aspects = sub_df["aspect"].dropna().astype(str).str.strip().str.lower()
    aspects = aspects[~aspects.isin(["", "unknown", "unspecified", "failed", "empty", "none"])]

    counts = aspects.value_counts().head(top_n).reset_index()
    counts.columns = ["aspect", "count"]
    return counts
