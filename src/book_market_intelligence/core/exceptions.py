"""
Application-wide domain exceptions for Book Market Intelligence Platform.
"""

class BookIntelError(Exception):
    """Base exception for all Book Market Intelligence domain errors."""
    pass


class ConfigurationError(BookIntelError):
    """Raised when environment variables or configurations are missing or invalid."""
    pass


class DataIngestionError(BookIntelError):
    """Raised when external data collectors encounter fatal API or network errors."""
    pass


class PreprocessingError(BookIntelError):
    """Raised when data transformation, cleaning, or validation fails."""
    pass


class AuthenticationError(BookIntelError):
    """Raised when authentication or authorization fails."""
    pass


class RAGRetrievalError(BookIntelError):
    """Raised when the vector store or retrieval engine fails."""
    pass


class ModelInferenceError(BookIntelError):
    """Raised when LLM calls or inference fails."""
    pass
