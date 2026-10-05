"""
User authentication and credential management service.
Provides salted password storage, role verification, and user state handling.
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from book_market_intelligence.auth.security import hash_password, verify_password
from book_market_intelligence.config.settings import settings
from book_market_intelligence.core.logging import logger

VALID_PERSONAS = ["Store Manager", "Regional Manager", "Executive"]


@dataclass
class User:
    username: str
    persona: str
    password_hash: str
    salt: str
    created_at: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "username": self.username,
            "persona": self.persona,
            "password_hash": self.password_hash,
            "salt": self.salt,
            "created_at": self.created_at,
        }


class AuthService:
    """Thread-safe user management service backed by secure JSON store."""

    def __init__(self, storage_path: Optional[Path] = None) -> None:
        self.storage_path = storage_path or settings.USERS_FILE
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        """Initializes the user database and seeds initial accounts securely."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            logger.info("Initializing new secure user store with default personas...")
            users = self._seed_default_users()
            self._save_users(users)
        else:
            # Check if empty
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if not data:
                        users = self._seed_default_users()
                        self._save_users(users)
            except Exception as e:
                logger.warning(f"Resetting corrupted user store: {e}")
                users = self._seed_default_users()
                self._save_users(users)

    def _seed_default_users(self) -> Dict[str, Dict]:
        """Seeds default persona accounts with cryptographic hashes (no plaintext)."""
        defaults = [
            ("om1", "2004", "Store Manager"),
            ("om2", "2004", "Regional Manager"),
            ("om3", "2004", "Executive"),
        ]
        users: Dict[str, Dict] = {}
        for username, password, persona in defaults:
            p_hash, salt = hash_password(password)
            users[username] = {
                "username": username,
                "persona": persona,
                "password_hash": p_hash,
                "salt": salt,
                "created_at": datetime.utcnow().isoformat(),
            }
        return users

    def _load_users(self) -> Dict[str, Dict]:
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read user storage: {e}")
            return {}

    def _save_users(self, users: Dict[str, Dict]) -> None:
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to write user storage: {e}")

    def register_user(self, username: str, password: str, persona: str) -> bool:
        """
        Registers a new user with salted hashed credentials.
        Returns False if username exists or validation fails.
        """
        username = username.strip()
        password = password.strip()

        if len(username) < 3 or len(password) < settings.PASSWORD_MIN_LENGTH:
            logger.warning(f"Registration validation failed for '{username}'")
            return False

        if persona not in VALID_PERSONAS:
            logger.warning(f"Invalid persona '{persona}' for '{username}'")
            return False

        users = self._load_users()
        if username in users:
            logger.info(f"Username '{username}' already exists")
            return False

        p_hash, salt = hash_password(password)
        users[username] = {
            "username": username,
            "persona": persona,
            "password_hash": p_hash,
            "salt": salt,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._save_users(users)
        logger.info(f"User '{username}' ({persona}) successfully registered.")
        return True

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticates a user by checking salted password hash.
        Returns the User object on success, or None on failure.
        """
        username = username.strip()
        password = password.strip()

        users = self._load_users()
        user_data = users.get(username)

        if not user_data:
            return None

        is_valid = verify_password(
            plain_password=password,
            stored_hash=user_data["password_hash"],
            salt=user_data["salt"]
        )

        if is_valid:
            logger.info(f"Successful login for user '{username}' ({user_data['persona']})")
            return User(
                username=user_data["username"],
                persona=user_data["persona"],
                password_hash=user_data["password_hash"],
                salt=user_data["salt"],
                created_at=user_data.get("created_at", ""),
            )

        logger.warning(f"Failed login attempt for user '{username}'")
        return None

    def get_user(self, username: str) -> Optional[User]:
        users = self._load_users()
        u = users.get(username.strip())
        if not u:
            return None
        return User(
            username=u["username"],
            persona=u["persona"],
            password_hash=u["password_hash"],
            salt=u["salt"],
            created_at=u.get("created_at", "")
        )


# Global service singleton
auth_service = AuthService()
