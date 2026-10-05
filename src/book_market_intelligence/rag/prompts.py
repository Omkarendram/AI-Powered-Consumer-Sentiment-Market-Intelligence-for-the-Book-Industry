"""
RAG prompt templates and query classification definitions.
"""

from typing import List
from book_market_intelligence.rag.vector_store import VectorDocument

MARKET_ANALYST_SYSTEM_PROMPT = """You are a Principal Market Intelligence Analyst for an enterprise book platform.
Analyze real consumer feedback to produce actionable, data-backed business insights for leadership.

Ground your answers strictly on the retrieved customer feedback below.
If the feedback lacks sufficient evidence to answer, state: "Insufficient consumer feedback data on this topic in the current repository."

Structure your response into 4 distinct executive sections:
1. 📌 Key Market Trend / Root Cause
2. 💬 Evidence from Consumer Feedback (cite direct quotes and sentiment tags)
3. ⚠️ Business & Revenue Impact (churn risk, store impact, catalog reputation)
4. 🚀 Recommended Actionable Next Step
"""


def build_rag_prompt(query: str, context_docs: List[VectorDocument]) -> str:
    """Formats retrieved context documents into structured LLM prompt."""
    blocks = []
    for i, doc in enumerate(context_docs, start=1):
        sentiment = doc.metadata.get("sentiment", "unknown").upper()
        source = doc.metadata.get("source", "feedback")
        topic = doc.metadata.get("topic", "general")
        aspect = doc.metadata.get("aspect", "")

        blocks.append(
            f"[Feedback #{i} | Channel: {source} | Sentiment: {sentiment} | Topic: {topic} | Aspect: {aspect}]\n"
            f"\"{doc.text}\""
        )

    context_str = "\n\n".join(blocks)

    return f"""Context Excerpts:
{context_str}

User Question:
{query}

Provide a structured, executive-grade analysis based strictly on the above evidence."""
