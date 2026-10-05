"""
Vector embedding providers for semantic search with zero-crash fallbacks.
"""

from abc import ABC, abstractmethod
from typing import List
import re
import numpy as np
from book_market_intelligence.core.logging import logger


class BaseEmbeddingProvider(ABC):
    """Abstract interface for document and query text embedding."""

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """Encodes a list of document strings into an (N, D) numpy array."""
        pass

    @abstractmethod
    def embed_query(self, text: str) -> np.ndarray:
        """Encodes a single query string into a (D,) numpy array."""
        pass


class LightweightTfidfEmbeddingProvider(BaseEmbeddingProvider):
    """
    High-performance, dependency-light semantic vectorizer.
    Uses sublinear term frequency with vocabulary hashing to produce normalized
    fixed-dimension embedding vectors without downloading heavy neural models.
    """

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    def _hash_token(self, token: str) -> int:
        h = 0
        for char in token:
            h = (h * 31 + ord(char)) % self.dim
        return h

    def _vectorize_text(self, text: str) -> np.ndarray:
        vec = np.zeros(self.dim, dtype=np.float32)
        tokens = re.findall(r"\b[a-z0-9]{2,}\b", text.lower())
        if not tokens:
            return vec

        for token in tokens:
            idx = self._hash_token(token)
            vec[idx] += 1.0

        # Sublinear scaling: log(1 + tf)
        vec = np.log1p(vec)

        # L2 Normalize
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm
        return vec

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        return np.vstack([self._vectorize_text(t) for t in texts])

    def embed_query(self, text: str) -> np.ndarray:
        return self._vectorize_text(text)


def get_embedding_provider() -> BaseEmbeddingProvider:
    """
    Factory function returning the best available embedding provider.
    Prefers SentenceTransformers if installed, otherwise uses lightweight provider.
    """
    try:
        from sentence_transformers import SentenceTransformer

        class SentenceTransformerProvider(BaseEmbeddingProvider):
            def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
                self.model = SentenceTransformer(model_name)

            def embed_documents(self, texts: List[str]) -> np.ndarray:
                embeddings = self.model.encode(texts, normalize_embeddings=True)
                return np.array(embeddings, dtype=np.float32)

            def embed_query(self, text: str) -> np.ndarray:
                embedding = self.model.encode(text, normalize_embeddings=True)
                return np.array(embedding, dtype=np.float32)

        logger.info("Using SentenceTransformer embeddings engine.")
        return SentenceTransformerProvider()
    except Exception:
        logger.info("Using lightweight vectorized embedding engine.")
        return LightweightTfidfEmbeddingProvider(dim=256)
