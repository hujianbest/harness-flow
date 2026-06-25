"""
Security utilities for authentication and authorization.
"""
from datetime import datetime, timedelta
from typing import Optional
import hashlib

from jose import JWTError, jwt

from app.core.config import get_settings

settings = get_settings()


def _hash_password_simple(password: str) -> str:
    """Simple password hash for MVP (use bcrypt in production)."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return _hash_password_simple(plain_password) == hashed_password


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return _hash_password_simple(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT access token."""
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None
