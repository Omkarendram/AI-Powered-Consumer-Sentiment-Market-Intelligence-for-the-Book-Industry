# AI-Powered Consumer Sentiment & Market Intelligence for the Book Industry

## 📌Project Overview

This project builds an AI-driven market intelligence system that analyzes large volumes of consumer feedback related to the book market (e-commerce, social media, and news) to uncover:

🔹Customer sentiment (positive / negative / neutral)

🔹Key topics and aspects (e.g., platform experience, story quality, pricing)

🔹Emerging trends and complaints

🔹Actionable business insights via a Retrieval-Augmented Generation (RAG) system

The system is designed to act as a smart assistant for market and product teams, enabling natural language querying over real customer feedback.

## 🧩Module 1: Data Collection & Preprocessing

📊 Data Sources

🔹YouTube comments related to book reviews

🔹News articles related to books, publishing, and reading trends

🔹Publicly available e-commerce/book metadata (Google Books API as a proxy source)

🛠 Tools & Libraries

🔸Python

🔸Requests

🔸Pandas

🔸NLTK

🔸Google YouTube Data API

🔸NewsAPI

### 💠Description

This module handles raw data ingestion from multiple sources and applies text cleaning and normalization to prepare the data for downstream ML tasks.
All raw text is unified into a common schema and stored as a cleaned corpus.

📤 Output

Raw data:

🔹data/raw/youtube_book_comments.csv

🔹data/raw/news_articles.csv

🔹data/raw/ecommerce_books.csv

Processed data:

🔹data/processed/cleaned_text.csv

## 🧠Module 2: Sentiment Analysis & Topic / Aspect Extraction

📌Description

This module enriches the cleaned feedback using an LLM-based pipeline to extract:

🔹Sentiment (positive / negative / neutral)

🔹Topic (e.g., platform_experience, story_quality, genre_preference)

🔹Aspect (specific issue or praise such as “app crashes”, “weak plot”)

This transforms raw feedback into a structured market intelligence dataset suitable for retrieval and analytics.

📤 Output

Enriched dataset:

🔹sentiment_analysis/book_market_sentiment_topics.csv

  (contains: clean_text, sentiment, topic, aspect)

### 🔎Module 3: RAG Pipeline & Insights Dashboards (Milestone 3)

📌Description

This module implements a Retrieval-Augmented Generation (RAG) pipeline to enable natural language querying over the enriched feedback corpus.
A prototype insights dashboard is built to visualize sentiment and topic trends.

## 🛠Tech Stack

🔸LangChain (RAG orchestration)

🔸ChromaDB (Vector Database; Pinecone-compatible architecture)

🔸HuggingFace Sentence Transformers (Embeddings)

🔸Groq API (LLM backend – LLaMA 3.1)

🔸Streamlit (Dashboard UI prototype)

📤 Output

▫️Vector database built from enriched feedback

▫️Working RAG-based Q&A system

▫️Prototype dashboards for:

▫️Sentiment distribution

▫️Topic trends

▫️Top complaints and themes

### 📈Current Project Status

✔ Data Collection & Preprocessing

✔ Sentiment Analysis & Topic / Aspect Extraction

✔ RAG Pipeline (LangChain + Vector DB + LLM)

🟡 Insights Dashboard (Streamlit prototype in progress)

⬜ Production API Deployment (FastAPI)

⬜ Alerting & Monitoring (Future Work)

### 🚀Future Enhancements

💠Brand-specific platform analysis (e.g., Amazon, Kindle, Goodreads)

💠Real-time data ingestion & streaming updates

💠Automated alerts for emerging negative trends

💠Deployment on cloud infrastructure

💠Switching vector backend to Pinecone for large-scale production use
