"""
Integration tests for the FastAPI REST API endpoints.
"""

from fastapi.testclient import TestClient
from book_market_intelligence.api.main import create_app

app = create_app()
client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "book-market-intelligence-api"


def test_sentiment_predict_endpoint():
    payload = {"text": "I absolutely love this novel, brilliant writing!"}
    response = client.post("/api/v1/sentiment/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"
    assert 0.0 <= data["confidence"] <= 1.0


def test_sentiment_batch_endpoint():
    payload = {
        "texts": [
            "Superb book and fast delivery",
            "Terrible customer service and damaged item"
        ]
    }
    response = client.post("/api/v1/sentiment/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["results"]) == 2


def test_analytics_overview_endpoint():
    response = client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_feedback" in data
    assert "positive_rate" in data
    assert "risk_ratio" in data


def test_rag_query_endpoint():
    payload = {
        "query": "What are the common complaints about book quality?",
        "top_k": 3
    }
    response = client.post("/api/v1/rag/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "retrieved_documents" in data
    assert len(data["answer"]) > 10
