"""
Unit tests for cryptographic security, password hashing, and user authentication.
"""

import pytest
from book_market_intelligence.auth.security import hash_password, verify_password, generate_salt


def test_salt_generation():
    salt1 = generate_salt()
    salt2 = generate_salt()
    assert salt1 != salt2
    assert len(salt1) >= 16


def test_password_hashing_and_verification():
    raw_pass = "SecurePass#2026"
    p_hash, salt = hash_password(raw_pass)

    assert p_hash != raw_pass
    assert len(p_hash) == 64  # SHA-256 hex digest length
    assert verify_password(raw_pass, p_hash, salt) is True
    assert verify_password("WrongPassword", p_hash, salt) is False


def test_different_salts_produce_different_hashes():
    raw_pass = "Enterprise2026"
    hash1, salt1 = hash_password(raw_pass)
    hash2, salt2 = hash_password(raw_pass)

    assert salt1 != salt2
    assert hash1 != hash2


def test_empty_password_raises():
    with pytest.raises(ValueError):
        hash_password("")


def test_auth_service_seeding_and_auth(temp_user_store):
    service = temp_user_store

    # Test seeded accounts
    u1 = service.authenticate_user("om1", "2004")
    assert u1 is not None
    assert u1.persona == "Store Manager"

    u2 = service.authenticate_user("om2", "2004")
    assert u2 is not None
    assert u2.persona == "Regional Manager"

    # Test invalid password
    bad = service.authenticate_user("om1", "wrong_pass")
    assert bad is None


def test_auth_service_registration(temp_user_store):
    service = temp_user_store

    # Register new user
    ok = service.register_user("new_analyst", "Secret123", "Executive")
    assert ok is True

    # Duplicate registration fails
    ok_dup = service.register_user("new_analyst", "Secret123", "Executive")
    assert ok_dup is False

    # Invalid persona fails
    ok_bad_persona = service.register_user("analyst2", "Secret123", "SuperAdmin")
    assert ok_bad_persona is False

    # Authenticate newly registered user
    user = service.authenticate_user("new_analyst", "Secret123")
    assert user is not None
    assert user.persona == "Executive"
