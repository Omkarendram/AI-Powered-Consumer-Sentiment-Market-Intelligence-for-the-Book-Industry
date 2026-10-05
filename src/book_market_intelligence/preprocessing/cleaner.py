"""
Text preprocessing and cleaning utilities for consumer feedback text.
"""

import re
from typing import Optional, Set

# Comprehensive built-in English stopwords list (zero external dependency requirement)
DEFAULT_STOPWORDS: Set[str] = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her",
    "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs",
    "themselves", "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while", "of", "at", "by", "for", "with",
    "about", "against", "between", "into", "through", "during", "before", "after",
    "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over",
    "under", "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "any", "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "s", "t", "can", "will", "just", "don", "should", "now"
}

def get_stopwords() -> Set[str]:
    """Retrieve NLTK stopwords if available, falling back to built-in list."""
    try:
        import nltk
        from nltk.corpus import stopwords
        try:
            return set(stopwords.words("english"))
        except LookupError:
            nltk.download("stopwords", quiet=True)
            return set(stopwords.words("english"))
    except Exception:
        return DEFAULT_STOPWORDS


STOPWORDS = get_stopwords()


def clean_text(text: Optional[str], remove_stopwords: bool = True) -> str:
    """
    Cleans raw review/article/comment text:
    - Normalizes case to lowercase
    - Strips URLs and hyper-references
    - Strips HTML tags and markdown
    - Strips non-alphanumeric punctuation
    - Collapses multiple whitespace characters
    - Optionally removes common English stopwords
    """
    if text is None:
        return ""

    text = str(text)
    if not text.strip():
        return ""

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Keep letters, numbers, and basic spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip()

    if remove_stopwords:
        tokens = [word for word in text.split() if word not in STOPWORDS and len(word) > 1]
        return " ".join(tokens)

    return text
