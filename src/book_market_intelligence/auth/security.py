"""
Cryptographic security and password hashing utilities.
Uses industry-standard PBKDF2-HMAC-SHA256 with random salting and constant-time verification.
"""

import hashlib
import hmac
import os
import secrets
from typing import Tuple, Optional


def generate_salt(length: int = 16) -> str:
    """Generate a cryptographically secure random hexadecimal salt."""
    return secrets.token_hex(length)


def hash_password(
    plain_password: str,
    salt: Optional[str] = None,
    iterations: int = 100_000
) -> Tuple[str, str]:
    """
    Hashes a password using PBKDF2-HMAC-SHA256 with a unique salt.

    Args:
        plain_password: The plaintext password string.
        salt: Optional hexadecimal salt. If not provided, a fresh salt is generated.
        iterations: Number of PBKDF2 iterations (default 100,000).

    Returns:
        A tuple of (hex_digest, salt).
    """
    if not plain_password:
        raise ValueError("Password cannot be empty")

    if salt is None:
        salt = generate_salt()

    salt_bytes = bytes.fromhex(salt) if len(salt) % 2 == 0 else salt.encode("utf-8")

    derived_key = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=plain_password.encode("utf-8"),
        salt=salt_bytes,
        iterations=iterations,
        dklen=32
    )

    return derived_key.hex(), salt


def verify_password(plain_password: str, stored_hash: str, salt: str, iterations: int = 100_000) -> bool:
    """
    Verifies a plaintext password against a stored PBKDF2 hash using constant-time comparison.
    """
    if not plain_password or not stored_hash or not salt:
        return False

    computed_hash, _ = hash_password(plain_password, salt=salt, iterations=iterations)
    return hmac.compare_digest(computed_hash, stored_hash)
