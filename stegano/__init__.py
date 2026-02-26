"""
stegano - A Python-based offline steganography toolkit

This package provides steganography capabilities for various media types:
- Images (PNG, JPEG, BMP) using LSB encoding
- Audio files (WAV) using LSB encoding
- Text files using whitespace/zero-width character encoding
- Optional AES-256 password-based encryption for hidden messages
"""

__version__ = "3.0.0"
__author__ = "Irfan Ali"
__email__ = "irfan.sec@example.com"

from .audio import decode_audio, encode_audio
from .crypto import decrypt_message, encrypt_message, is_encrypted
from .image import decode_image, encode_image
from .text import decode_text, encode_text

__all__ = [
    "encode_image",
    "decode_image",
    "encode_audio",
    "decode_audio",
    "encode_text",
    "decode_text",
    "encrypt_message",
    "decrypt_message",
    "is_encrypted",
]
