# 📁 Enterprise Project Structure & Technical Architecture

## 1. Directory Tree

```
AI-Powered-Consumer-Sentiment-Market-Intelligence-for-the-Book-Industry/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Automated testing, linting & syntax checks
│
├── deploy/
│   ├── Dockerfile.api                # Production Dockerfile for FastAPI backend
│   ├── Dockerfile.ui                 # Production Dockerfile for Streamlit dashboard
│   └── docker-compose.yml            # Multi-service composition
│
├── docs/
│   ├── ARCHITECTURE.md               # Enterprise architecture specification & diagrams
│   ├── API_DOCUMENTATION.md          # OpenAPI / Swagger REST endpoint reference
│   ├── RESULTS_GUIDE.md              # Analytics outcomes and metrics guide
│   ├── INSIGHTS.md                   # Market insights and executive takeaways
│   ├── PROJECT_STRUCTURE.md          # Project structure guide (this file)
│   ├── FILE_ORGANIZATION.md          # File organization reference
│   └── project_management/
│       └── Agile_Team_2.xlsx         # Sprint backlog, standups & retrospection
│
├── src/
│   └── book_market_intelligence/     # Enterprise Python Package
│       ├── __init__.py
│       ├── config/                   # Centralized configuration & environment loader
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── core/                     # Domain exceptions & structured logging
│       │   ├── __init__.py
│       │   ├── exceptions.py
│       │   └── logging.py
│       ├── auth/                     # Cryptographic salted PBKDF2 authentication
│       │   ├── __init__.py
│       │   ├── security.py
│       │   └── service.py
│       ├── ingestion/                # Multi-channel data ingestion collectors
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── youtube.py
│       │   ├── news.py
│       │   └── ecommerce.py
│       ├── preprocessing/            # NLP text cleaning, normalization & validator
│       │   ├── __init__.py
│       │   ├── cleaner.py
│       │   ├── validator.py
│       │   └── pipeline.py
│       ├── analytics/                # Aspect extraction, sentiment engine & metrics
│       │   ├── __init__.py
│       │   ├── metrics.py
│       │   ├── sentiment.py
│       │   └── topics.py
│       ├── rag/                      # Semantic retrieval & LLM synthesis engine
│       │   ├── __init__.py
│       │   ├── embeddings.py
│       │   ├── vector_store.py
│       │   ├── prompts.py
│       │   └── engine.py
│       ├── api/                      # Production FastAPI REST backend
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── schemas.py
│       │   └── routes/
│       │       ├── __init__.py
│       │       ├── health.py
│       │       ├── rag.py
│       │       ├── sentiment.py
│       │       └── analytics.py
│       └── ui/                       # Reusable UI components & dark theme
│           ├── __init__.py
│           ├── theme.py
│           ├── components.py
│           └── rag_widget.py
│
├── data/
│   ├── raw/                          # Raw scraped datasets
│   │   ├── ecommerce_books.csv
│   │   ├── news_articles.csv
│   │   └── youtube_book_comments.csv
│   └── processed/                    # Validated & enriched datasets
│       ├── cleaned_text.csv
│       ├── book_feedback.csv
│       ├── sentiment_analysis_results.csv
│       ├── sentiment_analysis_results_batch.csv
│       ├── book_market_sentiment_topics.csv
│       ├── llm_topic_results.csv
│       └── validated_cleaned_text.csv
│
├── pages/                            # Streamlit role-based multi-page dashboards
│   ├── Login.py                      # Salted PBKDF2 authentication
│   ├── Signup.py                     # User registration & persona selection
│   ├── Overview.py                   # Executive KPI overview & heatmaps
│   ├── Market_Insights.py            # Thematic topic & aspect breakdown
│   ├── Sentiment_Dashboard.py        # Granular sentiment tracking & inference tool
│   └── Alerts_Reports.py             # Risk ratio monitor & email incident alerting
│
├── tests/                            # Automated test suite (22 tests)
│   ├── conftest.py                   # Pytest fixtures & mock datasets
│   ├── unit/
│   │   ├── test_security.py
│   │   ├── test_preprocessing.py
│   │   ├── test_sentiment.py
│   │   └── test_rag.py
│   └── integration/
│       └── test_api.py
│
├── app.py                            # Streamlit entrypoint
├── cli.py                            # Unified Command-Line Interface
├── pyproject.toml                    # Modern PEP 517/621 packaging metadata
├── requirements.txt                  # Production dependencies (clean UTF-8)
├── requirements-dev.txt              # Testing and quality assurance dependencies
├── .env.example                      # Production environment template
└── README.md                         # Enterprise documentation front page
```
