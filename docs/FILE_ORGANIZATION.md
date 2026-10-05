# 📁 File Organization Reference Guide

## Overview

The repository has been restructured from loose scripts and misplaced files into a cohesive, decoupled **enterprise architecture** adhering to standard Python packaging, Twelve-Factor application principles, and production data science conventions.

---

## 🏛️ Module Mapping

| Previous Location | New Enterprise Location | Purpose & Responsibility |
| :--- | :--- | :--- |
| `users.csv` (plaintext passwords) | **`data/users.json`** + **`src/.../auth/`** | Cryptographically salted PBKDF2 hashing (100,000 rounds). Plaintext credentials eliminated. |
| `Agile_Team_2.xlsx` (in root) | **`docs/project_management/`** | Project tracking, sprint backlogs, standup logs, and retrospectives. |
| `insights.md` (in root) | **`docs/INSIGHTS.md`** | High-level market insights and qualitative findings. |
| `RESULTS_GUIDE.md` (in root) | **`docs/RESULTS_GUIDE.md`** | Guide to data pipeline outputs and metric interpretations. |
| `tempCodeRunnerFile.py` (in root) | **REMOVED** | Stale editor artifact completely purged. |
| `sentiment_analysis/*.csv` | **`data/processed/`** | Centralized processed data folder. Code directories contain only Python modules. |
| `topic_modeling/*.csv` | **`data/processed/`** | Centralized processed data folder. Code directories contain only Python modules. |
| `rag/api.py` (commented out) | **`src/.../api/`** | Fully functional FastAPI REST backend with Pydantic v2 schemas and Swagger `/docs`. |
| `rag/rag_app.py` (FakeEmbeddings) | **`src/.../rag/`** | True vector embeddings (SentenceTransformers / sublinear TF-IDF) with cosine similarity and Groq LLM synthesis. |
| `theme.py` & `utils/*.py` | **`src/.../ui/`** | Modular Streamlit UI components, session guards, and responsive dark theme CSS. |
| Ad-hoc scripts | **`cli.py`** | Unified CLI for preprocessing, sentiment inference, RAG queries, testing, and web server execution. |
| None | **`tests/`** | 22 comprehensive automated tests with pytest covering unit, RAG, and API integration. |
| None | **`deploy/`** | Production multi-stage Dockerfiles and `docker-compose.yml`. |
| None | **`.github/workflows/ci.yml`** | GitHub Actions automated test & lint CI pipeline. |
