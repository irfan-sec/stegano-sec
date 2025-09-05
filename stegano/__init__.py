"""
stegano - A Python-based offline steganography toolkit

This package provides steganography capabilities for various media types:
- Images (PNG, JPEG) using LSB encoding
- Audio files (WAV) using LSB encoding  
- Text files using whitespace/zero-width character encoding
"""

__version__ = "1.0.0"
__author__ = "Irfan Ali"
__email__ = "irfan.sec@example.com"

from .image import encode_image, decode_image
from .audio import encode_audio, decode_audio
from .text import encode_text, decode_text

__all__ = [
    'encode_image', 'decode_image',
    'encode_audio', 'decode_audio', 
    'encode_text', 'decode_text'
]