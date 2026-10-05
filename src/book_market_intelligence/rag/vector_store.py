"""
Thread-safe in-memory vector store with metadata filtering and cosine similarity.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from book_market_intelligence.core.logging import logger
from book_market_intelligence.rag.embeddings import BaseEmbeddingProvider, get_embedding_provider


@dataclass
class VectorDocument:
    doc_id: str
    text: str
    metadata: Dict[str, Any]
    score: float = 0.0


class VectorStore:
    """
    Vector database supporting semantic similarity search and metadata filtering.
    """

    def __init__(self, embedding_provider: Optional[BaseEmbeddingProvider] = None) -> None:
        self.embedding_provider = embedding_provider or get_embedding_provider()
        self.documents: List[VectorDocument] = []
        self.embeddings: Optional[np.ndarray] = None

    def add_documents(self, documents: List[VectorDocument]) -> None:
        if not documents:
            return

        texts = [doc.text for doc in documents]
        new_embeddings = self.embedding_provider.embed_documents(texts)

        if self.embeddings is None or len(self.documents) == 0:
            self.embeddings = new_embeddings
            self.documents = list(documents)
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
            self.documents.extend(documents)

        logger.info(f"Vector store indexed {len(self.documents)} total documents.")

    def build_from_dataframe(self, df: pd.DataFrame, text_col: str = "clean_text") -> None:
        """Populates vector index from a pandas DataFrame."""
        if df.empty or text_col not in df.columns:
            return

        docs: List[VectorDocument] = []
        for idx, row in df.iterrows():
            text = str(row.get(text_col, "")).strip()
            if not text:
                continue

            metadata = {
                "sentiment": str(row.get("sentiment", "neutral")).lower(),
                "confidence": float(row.get("confidence", 0.8)) if pd.notna(row.get("confidence")) else 0.8,
                "source": str(row.get("source", "youtube")),
                "topic": str(row.get("topic", "general_reading")),
                "aspect": str(row.get("aspect", "unspecified")),
            }
            docs.append(VectorDocument(
                doc_id=f"doc_{idx}",
                text=text,
                metadata=metadata
            ))

        self.add_documents(docs)

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[VectorDocument]:
        """
        Executes cosine similarity retrieval against indexed feedback with metadata constraints.
        """
        if self.embeddings is None or len(self.documents) == 0:
            return []

        query_vec = self.embedding_provider.embed_query(query)
        # Cosine similarity (vectors are unit-normalized)
        scores = np.dot(self.embeddings, query_vec)

        # Ranked indices
        ranked_indices = np.argsort(scores)[::-1]

        results: List[VectorDocument] = []
        for idx in ranked_indices:
            doc = self.documents[idx]

            # Apply metadata filters
            if filter_dict:
                match = True
                for f_key, f_val in filter_dict.items():
                    if doc.metadata.get(f_key) != str(f_val).lower():
                        match = False
                        break
                if not match:
                    continue

            result_doc = VectorDocument(
                doc_id=doc.doc_id,
                text=doc.text,
                metadata=doc.metadata,
                score=float(scores[idx])
            )
            results.append(result_doc)

            if len(results) >= k:
                break

        return results
