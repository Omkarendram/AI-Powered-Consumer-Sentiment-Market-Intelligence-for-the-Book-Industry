"""
Backward compatibility layer for RAG application logic.
Delegates to book_market_intelligence.rag.engine.rag_engine.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.rag.engine import rag_engine


def answer_query(query: str) -> str:
    """Answers market queries using the RAG engine."""
    result = rag_engine.query(query)
    return result.answer


def main():
    print("\n✅ RAG system ready! (CLI mode)")
    print("Ask questions (type 'exit' to quit)\n")

    while True:
        try:
            query = input("Ask: ")
            if query.lower() in ["exit", "quit", "q"]:
                break
            if not query.strip():
                continue
            answer = answer_query(query)
            print("\n🤖 Answer:\n", answer)
            print("-" * 60)
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()
