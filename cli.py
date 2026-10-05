#!/usr/bin/env python3
"""
Unified Command-Line Interface (CLI) for Book Market Intelligence Platform.
"""

import sys
import argparse
from pathlib import Path

# Add src/ to path so local imports resolve cleanly
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


def cmd_preprocess(args):
    from book_market_intelligence.preprocessing.pipeline import run_preprocessing_pipeline
    print("▶ Running end-to-end data preprocessing pipeline...")
    df = run_preprocessing_pipeline()
    print(f"✓ Completed. Clean records: {len(df)}")


def cmd_sentiment(args):
    from book_market_intelligence.analytics.sentiment import sentiment_analyzer
    from book_market_intelligence.config.settings import settings
    import pandas as pd

    input_path = settings.processed_cleaned_text_path
    output_path = settings.processed_sentiment_results_path

    if not input_path.exists():
        print(f"✗ Input file not found: {input_path}. Run 'preprocess' first.")
        return

    print(f"▶ Loading {input_path}...")
    df = pd.read_csv(input_path)
    limit = args.limit or len(df)
    texts = df["clean_text"].iloc[:limit].tolist()

    print(f"▶ Analyzing sentiment for {len(texts)} texts...")
    sentiments, confidences = sentiment_analyzer.analyze_batch(texts)

    result_df = df.iloc[:limit].copy()
    result_df["sentiment"] = sentiments
    result_df["confidence"] = confidences

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result_df.to_csv(output_path, index=False)
    print(f"✓ Saved results to {output_path}")


def cmd_rag(args):
    from book_market_intelligence.rag.engine import rag_engine
    query = args.query or "What are the most common complaints regarding delivery?"
    print(f"▶ Querying RAG system: '{query}'\n")
    res = rag_engine.query(query)
    print(f"Query Classification: {res.query_type}")
    print(f"Evidence Sources Retrieved: {len(res.retrieved_documents)}")
    print("\n" + "=" * 60)
    print(res.answer)
    print("=" * 60)


def cmd_serve(args):
    import uvicorn
    from book_market_intelligence.config.settings import settings
    port = args.port or settings.PORT
    host = args.host or settings.HOST
    print(f"▶ Starting FastAPI backend on http://{host}:{port}...")
    uvicorn.run("book_market_intelligence.api.main:app", host=host, port=port, reload=args.reload)


def cmd_dashboard(args):
    import subprocess
    print("▶ Starting Streamlit Dashboard...")
    subprocess.run(["streamlit", "run", "app.py", "--server.port", str(args.port or 8501)])


def cmd_test(args):
    import pytest
    print("▶ Executing automated test suite with pytest...")
    retcode = pytest.main(["-v", "tests"])
    sys.exit(retcode)


def main():
    parser = argparse.ArgumentParser(
        description="Book Market Intelligence Platform - Unified CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Preprocess
    p_prep = subparsers.add_parser("preprocess", help="Run multi-channel data ingestion and text cleaning")
    p_prep.set_defaults(func=cmd_preprocess)

    # Sentiment
    p_sent = subparsers.add_parser("sentiment", help="Run batch sentiment analysis")
    p_sent.add_argument("--limit", type=int, default=None, help="Number of records to process")
    p_sent.set_defaults(func=cmd_sentiment)

    # RAG
    p_rag = subparsers.add_parser("rag", help="Query the RAG market intelligence assistant")
    p_rag.add_argument("--query", "-q", type=str, required=True, help="Question to ask the RAG engine")
    p_rag.set_defaults(func=cmd_rag)

    # Serve
    p_serve = subparsers.add_parser("serve", help="Launch FastAPI REST backend")
    p_serve.add_argument("--host", type=str, default="0.0.0.0", help="Host interface")
    p_serve.add_argument("--port", "-p", type=int, default=8000, help="Listening port")
    p_serve.add_argument("--reload", action="store_true", help="Enable live code reloading")
    p_serve.set_defaults(func=cmd_serve)

    # Dashboard
    p_dash = subparsers.add_parser("dashboard", help="Launch Streamlit Analytics Dashboard")
    p_dash.add_argument("--port", "-p", type=int, default=8501, help="Dashboard port")
    p_dash.set_defaults(func=cmd_dashboard)

    # Test
    p_test = subparsers.add_parser("test", help="Execute automated test suite")
    p_test.set_defaults(func=cmd_test)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
