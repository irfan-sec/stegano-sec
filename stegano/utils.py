"""
Utility functions for the steganography toolkit
"""

import os
from pathlib import Path
from typing import Optional, Union


def validate_file_exists(filepath: Union[str, Path]) -> bool:
    """Check if a file exists and is readable

    Args:
        filepath: Path to the file to check

    Returns:
        True if file exists and is readable

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If path is not a file
        PermissionError: If file is not readable
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"File is not readable: {filepath}")
    return True


def validate_output_path(filepath: Union[str, Path]) -> bool:
    """Check if output path is writable

    Args:
        filepath: Path to the output file

    Returns:
        True if output path is writable

    Raises:
        FileNotFoundError: If output directory doesn't exist
        PermissionError: If output directory is not writable
    """
    path = Path(filepath).resolve()
    output_dir = path.parent

    if not output_dir.exists():
        raise FileNotFoundError(
            f"Output directory does not exist: {output_dir}"
        )
    if not os.access(output_dir, os.W_OK):
        raise PermissionError(
            f"Output directory is not writable: {output_dir}"
        )
    return True


def string_to_binary(text: str) -> str:
    """Convert string to binary representation

    Args:
        text: String to convert

    Returns:
        Binary representation as string
    """
    return "".join(format(ord(char), "08b") for char in text)


def binary_to_string(binary: str) -> str:
    """Convert binary representation back to string

    Args:
        binary: Binary string to convert

    Returns:
        Decoded string
    """
    # Split binary into 8-bit chunks
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i : i + 8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return "".join(chars)


def add_delimiter(
    binary_data: str, delimiter: str = "1111111111111110"
) -> str:
    """Add delimiter to mark end of hidden data

    Args:
        binary_data: Binary data to append delimiter to
        delimiter: Binary delimiter string

    Returns:
        Binary data with delimiter appended
    """
    return binary_data + delimiter


def find_delimiter(
    binary_data: str, delimiter: str = "1111111111111110"
) -> str:
    """Find delimiter in binary data and return data before it

    Args:
        binary_data: Binary string to search in
        delimiter: Binary delimiter to find

    Returns:
        Binary data before the delimiter
    """
    delimiter_pos = binary_data.find(delimiter)
    if delimiter_pos != -1:
        return binary_data[:delimiter_pos]
    return binary_data


def get_file_extension(filepath: Union[str, Path]) -> str:
    """Get file extension in lowercase

    Args:
        filepath: Path to file

    Returns:
        File extension in lowercase (e.g., '.png')
    """
    return Path(filepath).suffix.lower()


def is_valid_image_format(filepath: Union[str, Path]) -> bool:
    """Check if file has valid image extension

    Args:
        filepath: Path to check

    Returns:
        True if file has a valid image extension
    """
    valid_extensions = [".png", ".jpg", ".jpeg"]
    return get_file_extension(filepath) in valid_extensions


def is_valid_audio_format(filepath: Union[str, Path]) -> bool:
    """Check if file has valid audio extension

    Args:
        filepath: Path to check

    Returns:
        True if file has a valid audio extension
    """
    valid_extensions = [".wav"]
    return get_file_extension(filepath) in valid_extensions


def calculate_capacity(width: int, height: int, channels: int = 3) -> int:
    """Calculate maximum capacity for LSB steganography in images

    Args:
        width: Image width in pixels
        height: Image height in pixels
        channels: Number of color channels (default: 3 for RGB)

    Returns:
        Maximum number of characters that can be hidden
    """
    # Each pixel can hide 1 bit per channel
    total_bits = width * height * channels
    # Convert to characters (8 bits per char) minus delimiter
    return (total_bits // 8) - 2  # Reserve space for delimiter


def prepare_message_from_file(
    message: Optional[str], file_path: Optional[Union[str, Path]]
) -> str:
    """
    Prepare message for encoding by reading from file if needed.

    Args:
        message (str): Direct message text
        file_path (str): Path to file containing message (optional)

    Returns:
        str: Message content

    Raises:
        FileNotFoundError: If file_path is provided but doesn't exist
        ValueError: If no message is provided
    """
    if file_path:
        validate_file_exists(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            message = f.read()

    if not message:
        raise ValueError("Message cannot be empty")

    return message


def decode_binary_message(
    binary_message: str, input_path: Union[str, Path]
) -> Optional[str]:
    """
    Convert extracted binary message to text with error handling.

    Args:
        binary_message (str): Binary string extracted from media
        input_path (str): Path to input file for logging

    Returns:
        str or None: Decoded message or None if decoding failed
    """
    # Find delimiter and extract message
    binary_message = find_delimiter(binary_message)

    if not binary_message:
        print("✗ No hidden message found or message corrupted")
        return None

    # Convert binary to text
    try:
        decoded_message = binary_to_string(binary_message)
        print(f"✓ Message successfully decoded from {input_path}")
        print(f"  Message length: {len(decoded_message)} characters")
        return decoded_message

    except (UnicodeDecodeError, ValueError, AttributeError) as e:
        print(f"✗ Failed to convert binary to text: {str(e)}")
        return None
