"""
Unit tests for the RAG engine, vector store, and query classification.
"""

from book_market_intelligence.rag.engine import RAGEngine
from book_market_intelligence.rag.vector_store import VectorStore, VectorDocument


def test_rag_query_classification():
    engine = RAGEngine()

    assert engine.classify_query("Why are customers complaining about delivery?") == "negative"
    assert engine.classify_query("What do readers love the most?") == "positive"
    assert engine.classify_query("Summary of market signals") == "general"


def test_vector_store_retrieval():
    store = VectorStore()
    docs = [
        VectorDocument(doc_id="1", text="fast shipping and excellent book condition", metadata={"sentiment": "positive"}),
        VectorDocument(doc_id="2", text="app keeps crashing when opening audiobook", metadata={"sentiment": "negative"}),
        VectorDocument(doc_id="3", text="great plot and interesting character development", metadata={"sentiment": "positive"}),
        VectorDocument(doc_id="4", text="poor packaging pages were ripped", metadata={"sentiment": "negative"}),
    ]
    store.add_documents(docs)

    # Search for audio app crash
    res = store.similarity_search("audiobook crash problem", k=2)
    assert len(res) > 0
    assert "audiobook" in res[0].text or "crashing" in res[0].text

    # Filtered search for positive only
    res_pos = store.similarity_search("delivery shipping", k=2, filter_dict={"sentiment": "positive"})
    assert all(d.metadata["sentiment"] == "positive" for d in res_pos)
