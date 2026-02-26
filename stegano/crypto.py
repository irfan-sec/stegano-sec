"""
Cryptographic utilities for stegano-sec

Provides password-based authenticated encryption using Fernet
(AES-128-CBC + HMAC-SHA256) with PBKDF2 key derivation for securing
hidden messages.
"""

import base64
import os
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Prefix to identify encrypted content
ENCRYPTED_PREFIX = "STEGENC1:"

# PBKDF2 iterations for key derivation
PBKDF2_ITERATIONS = 600_000


def _derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a password and salt.

    Args:
        password: User-provided password
        salt: Random salt for key derivation

    Returns:
        URL-safe base64 encoded 32-byte key
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def encrypt_message(message: str, password: str) -> str:
    """Encrypt a message with a password using authenticated encryption.

    Uses Fernet (AES-128-CBC with HMAC-SHA256) for authenticated encryption.

    Args:
        message: Plaintext message to encrypt
        password: Password for encryption

    Returns:
        Encrypted message string with STEGENC1: prefix
    """
    salt = os.urandom(16)
    key = _derive_key(password, salt)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode("utf-8"))
    # Combine salt + encrypted token, then base64 encode
    combined = base64.urlsafe_b64encode(salt + encrypted)
    return ENCRYPTED_PREFIX + combined.decode("ascii")


def decrypt_message(data: str, password: str) -> Optional[str]:
    """Decrypt a message that was encrypted with encrypt_message.

    Args:
        data: Encrypted message string (with or without STEGENC1: prefix)
        password: Password for decryption

    Returns:
        Decrypted plaintext message, or None if decryption fails
    """
    if not data.startswith(ENCRYPTED_PREFIX):
        return data  # Not encrypted, return as-is

    try:
        encoded = data[len(ENCRYPTED_PREFIX) :]
        raw = base64.urlsafe_b64decode(encoded)
        salt = raw[:16]
        encrypted_token = raw[16:]
        key = _derive_key(password, salt)
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_token).decode("utf-8")
    except (InvalidToken, ValueError, UnicodeDecodeError):
        return None


def is_encrypted(data: str) -> bool:
    """Check if a message appears to be encrypted.

    Args:
        data: Message string to check

    Returns:
        True if the message has the encryption prefix
    """
    return data.startswith(ENCRYPTED_PREFIX)
