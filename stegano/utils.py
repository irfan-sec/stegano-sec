"""
Utility functions for the steganography toolkit
"""

import os


def validate_file_exists(filepath):
    """Check if a file exists and is readable"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    if not os.path.isfile(filepath):
        raise ValueError(f"Path is not a file: {filepath}")
    if not os.access(filepath, os.R_OK):
        raise PermissionError(f"File is not readable: {filepath}")
    return True


def validate_output_path(filepath):
    """Check if output path is writable"""
    output_dir = os.path.dirname(os.path.abspath(filepath))
    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory does not exist: {output_dir}")
    if not os.access(output_dir, os.W_OK):
        raise PermissionError(f"Output directory is not writable: {output_dir}")
    return True


def string_to_binary(text):
    """Convert string to binary representation"""
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_string(binary):
    """Convert binary representation back to string"""
    # Split binary into 8-bit chunks
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)


def add_delimiter(binary_data, delimiter="1111111111111110"):
    """Add delimiter to mark end of hidden data"""
    return binary_data + delimiter


def find_delimiter(binary_data, delimiter="1111111111111110"):
    """Find delimiter in binary data and return data before it"""
    delimiter_pos = binary_data.find(delimiter)
    if delimiter_pos != -1:
        return binary_data[:delimiter_pos]
    return binary_data


def get_file_extension(filepath):
    """Get file extension in lowercase"""
    return os.path.splitext(filepath)[1].lower()


def is_valid_image_format(filepath):
    """Check if file has valid image extension"""
    valid_extensions = ['.png', '.jpg', '.jpeg']
    return get_file_extension(filepath) in valid_extensions


def is_valid_audio_format(filepath):
    """Check if file has valid audio extension"""
    valid_extensions = ['.wav']
    return get_file_extension(filepath) in valid_extensions


def calculate_capacity(width, height, channels=3):
    """Calculate maximum capacity for LSB steganography in images"""
    # Each pixel can hide 1 bit per channel
    total_bits = width * height * channels
    # Convert to characters (8 bits per char) minus delimiter
    return (total_bits // 8) - 2  # Reserve space for delimiter