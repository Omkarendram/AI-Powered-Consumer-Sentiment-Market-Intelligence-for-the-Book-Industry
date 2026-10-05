"""
RAG orchestration engine coordinating retrieval, query classification, and LLM synthesis.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger
from book_market_intelligence.rag.vector_store import VectorStore, VectorDocument
from book_market_intelligence.rag.prompts import MARKET_ANALYST_SYSTEM_PROMPT, build_rag_prompt


@dataclass
class RAGResult:
    query: str
    answer: str
    retrieved_documents: List[Dict[str, Any]]
    query_type: str


class RAGEngine:
    """
    Retrieval-Augmented Generation engine for book market consumer feedback.
    """

    def __init__(self, data_path: Optional[Path] = None) -> None:
        self.data_path = data_path or settings.processed_topics_path
        self._vector_store: Optional[VectorStore] = None
        self._groq_client = None

        if settings.GROQ_API_KEY:
            try:
                from groq import Groq
                self._groq_client = Groq(api_key=settings.GROQ_API_KEY)
            except Exception as e:
                logger.warning(f"Groq client init failed: {e}")

    def _get_vector_store(self) -> VectorStore:
        """Lazy-loads and caches vector store."""
        if self._vector_store is None:
            logger.info("Initializing vector store from dataset...")
            store = VectorStore()

            # Try primary dataset or fallback
            target = self.data_path
            if not target.exists():
                target = settings.processed_feedback_path
            if not target.exists():
                target = settings.processed_cleaned_text_path

            if target.exists():
                df = pd.read_csv(target)
                store.build_from_dataframe(df)
            else:
                logger.warning(f"No feedback dataset found at {target} to index into RAG.")

            self._vector_store = store

        return self._vector_store

    def classify_query(self, query: str) -> str:
        """Classifies intent to optimize retrieval filtering."""
        q = query.lower()
        if any(term in q for term in ["complain", "issue", "problem", "defect", "bad", "poor", "negative", "hate", "bug", "crash", "delay", "terrible", "worst", "waste"]):
            return "negative"
        if any(term in q for term in ["praise", "good", "love", "favorite", "favourite", "positive", "best", "recommend", "great", "excellent", "enjoy"]):
            return "positive"
        return "general"

    def _offline_synthesis(self, query: str, docs: List[VectorDocument], query_type: str) -> str:
        """Generates structured market analyst response when offline without LLM keys."""
        if not docs:
            return (
                "### 📌 Market Intelligence Summary\n\n"
                "**Insufficient consumer feedback data** found matching your query in the current dataset.\n"
                "Please verify the query terms or expand data ingestion."
            )

        topics_found = list({d.metadata.get("topic", "general_reading") for d in docs})
        aspects_found = list({d.metadata.get("aspect", "") for d in docs if d.metadata.get("aspect")})

        evidence_bullets = "\n".join([
            f"- **[{d.metadata.get('sentiment', 'neutral').upper()} | {d.metadata.get('topic', 'reading')}]**: \"{d.text[:140]}...\""
            for d in docs[:3]
        ])

        return f"""### 📌 Key Market Trend / Root Cause
Consumer sentiment reflects primary themes around **{', '.join(topics_found[:2])}** with recurring emphasis on *{', '.join(aspects_found[:2]) if aspects_found else 'product satisfaction'}*.

### 💬 Evidence from Consumer Feedback
{evidence_bullets}

### ⚠️ Business & Revenue Impact
- Reader churn risk is elevated if recurring negative aspects ({', '.join(aspects_found[:2]) if aspects_found else 'usability issues'}) are left unaddressed.
- Catalog trust and NPS are directly impacted by mismatch between marketing hype and actual content delivery.

### 🚀 Recommended Actionable Next Step
1. Coordinate with publishing and logistics partners to address delivery/quality feedback.
2. Align editorial recommendation tags to prevent reader expectation mismatch.
3. Track sentiment trajectory weekly in the Alerts & Reports dashboard."""

    def query(self, user_query: str, top_k: Optional[int] = None) -> RAGResult:
        """
        Executes hybrid retrieval and synthesizes business insight.
        """
        k = top_k or settings.RAG_TOP_K
        store = self._get_vector_store()
        query_type = self.classify_query(user_query)

        filter_dict = None
        if query_type in ["negative", "positive"]:
            filter_dict = {"sentiment": query_type}

        retrieved = store.similarity_search(user_query, k=k, filter_dict=filter_dict)

        # Fallback to unfiltered if filtered search returned too few results
        if len(retrieved) < 2 and filter_dict is not None:
            retrieved = store.similarity_search(user_query, k=k)

        # Generate answer with Groq LLM if available
        if self._groq_client:
            prompt = build_rag_prompt(user_query, retrieved)
            try:
                response = self._groq_client.chat.completions.create(
                    model=settings.GROQ_FALLBACK_MODEL,
                    messages=[
                        {"role": "system", "content": MARKET_ANALYST_SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=450
                )
                answer_text = response.choices[0].message.content.strip()
            except Exception as e:
                logger.warning(f"Groq API synthesis failed: {e}. Using deterministic synthesis.")
                answer_text = self._offline_synthesis(user_query, retrieved, query_type)
        else:
            answer_text = self._offline_synthesis(user_query, retrieved, query_type)

        doc_dicts = [
            {
                "text": d.text,
                "score": round(d.score, 3),
                "metadata": d.metadata
            }
            for d in retrieved
        ]

        return RAGResult(
            query=user_query,
            answer=answer_text,
            retrieved_documents=doc_dicts,
            query_type=query_type
        )


# Global singleton engine
rag_engine = RAGEngine()
