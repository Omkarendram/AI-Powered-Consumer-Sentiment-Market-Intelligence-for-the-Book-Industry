# 🌐 REST API Reference Guide

The **Book Market Intelligence REST API** is built using FastAPI and conforms to OpenAPI 3.1 standards.
When running locally, interactive documentation is available at `http://localhost:8000/docs`.

---

## Base URL
```
http://localhost:8000
```

---

## 1. System & Health

### `GET /health`
Returns system operational state, application version, and environment.

**Response:** `200 OK`
```json
{
  "status": "ok",
  "version": "2.0.0",
  "environment": "production",
  "service": "book-market-intelligence-api"
}
```

---

## 2. Sentiment Analysis

### `POST /api/v1/sentiment/predict`
Evaluates a single customer review or comment and returns sentiment classification with confidence score.

**Request Body:**
```json
{
  "text": "The delivery was on time and the book is in immaculate condition! Love it."
}
```

**Response:** `200 OK`
```json
{
  "text": "The delivery was on time and the book is in immaculate condition! Love it.",
  "sentiment": "positive",
  "confidence": 0.88
}
```

---

### `POST /api/v1/sentiment/batch`
Batch sentiment inference across multiple consumer statements.

**Request Body:**
```json
{
  "texts": [
    "Fantastic novel, could not put it down!",
    "Pages arrived torn and binding was damaged."
  ]
}
```

**Response:** `200 OK`
```json
{
  "total": 2,
  "results": [
    {
      "text": "Fantastic novel, could not put it down!",
      "sentiment": "positive",
      "confidence": 0.85
    },
    {
      "text": "Pages arrived torn and binding was damaged.",
      "sentiment": "negative",
      "confidence": 0.90
    }
  ]
}
```

---

## 3. Market Intelligence RAG

### `POST /api/v1/rag/query`
Executes semantic retrieval across consumer feedback corpus and synthesizes structured executive market intelligence.

**Request Body:**
```json
{
  "query": "Why are readers complaining about shipping and delivery?",
  "top_k": 5
}
```

**Response:** `200 OK`
```json
{
  "query": "Why are readers complaining about shipping and delivery?",
  "answer": "### 📌 Key Market Trend / Root Cause\nPrimary consumer friction centers on delivery delays and print binding defects...",
  "query_type": "negative",
  "retrieved_documents": [
    {
      "text": "packaging was poor and pages arrived damaged...",
      "score": 0.812,
      "metadata": {
        "sentiment": "negative",
        "topic": "delivery",
        "aspect": "damaged binding",
        "source": "ecommerce"
      }
    }
  ]
}
```

---

## 4. Analytics & KPIs

### `GET /api/v1/analytics/overview`
Returns high-level business intelligence metrics and sentiment ratios.

**Response:** `200 OK`
```json
{
  "total_feedback": 2178,
  "positive_count": 930,
  "negative_count": 608,
  "neutral_count": 640,
  "positive_rate": 42.7,
  "negative_rate": 27.91,
  "neutral_rate": 29.38,
  "average_confidence": 0.74,
  "risk_ratio": 0.2791,
  "risk_level": "ELEVATED"
}
```

### `GET /api/v1/analytics/topics`
Returns top customer topics with volume and negative feedback percentages.

**Response:** `200 OK`
```json
[
  {
    "topic": "general_reading",
    "total_count": 1054,
    "negative_rate": 21.2
  },
  {
    "topic": "story_quality",
    "total_count": 482,
    "negative_rate": 34.6
  }
]
```
