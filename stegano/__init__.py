"""
stegano - A Python-based offline steganography toolkit

This package provides steganography capabilities for various media types:
- Images (PNG, JPEG) using LSB encoding
- Audio files (WAV) using LSB encoding
- Text files using whitespace/zero-width character encoding
"""

__version__ = "2.0.0"
__author__ = "Irfan Ali"
__email__ = "irfan.sec@example.com"

from .audio import decode_audio, encode_audio
from .image import decode_image, encode_image
from .text import decode_text, encode_text

__all__ = [
    "encode_image",
    "decode_image",
    "encode_audio",
    "decode_audio",
    "encode_text",
    "decode_text",
]
