"""
Backward compatibility layer for user authentication.
Delegates to book_market_intelligence.auth.service.auth_service with salted PBKDF2 hashing.
"""

import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from book_market_intelligence.auth.service import auth_service


def signup(username: str, password: str, persona: str) -> bool:
    """Creates a user account using secure salted cryptographic hashing."""
    return auth_service.register_user(username, password, persona)


def login(username: str, password: str) -> Optional[str]:
    """Authenticates credentials and returns the user persona, or None."""
    user = auth_service.authenticate_user(username, password)
    return user.persona if user else None
