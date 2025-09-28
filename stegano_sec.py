#!/usr/bin/env python3
"""
stegano-sec: A Python-based offline steganography toolkit

Main CLI interface for encoding and decoding messages in various media formats.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import after path modification
# pylint: disable=wrong-import-position
from stegano import (
    decode_audio,
    decode_image,
    decode_text,
    encode_audio,
    encode_image,
    encode_text,
)
from stegano.audio import get_audio_capacity
from stegano.image import get_image_capacity
from stegano.utils import get_file_extension


def detect_file_type(filepath: str) -> str:
    """Detect file type based on extension

    Args:
        filepath: Path to the file

    Returns:
        File type: 'image', 'audio', 'text', or 'unknown'
    """
    ext = get_file_extension(filepath)

    if ext in [".png", ".jpg", ".jpeg"]:
        return "image"
    if ext in [".wav"]:
        return "audio"
    if ext in [".txt", ".md"]:
        return "text"
    return "unknown"


def encode_command(args: argparse.Namespace) -> bool:
    """Handle encode command

    Args:
        args: Parsed command line arguments

    Returns:
        True if encoding was successful, False otherwise
    """
    # Detect input file type
    file_type = detect_file_type(args.input)

    if file_type == "unknown":
        print(f"✗ Unsupported file format: {get_file_extension(args.input)}")
        print(
            "  Supported formats: PNG, JPEG (images), WAV (audio), TXT, MD (text)"
        )
        return False

    # Validate that we have either message or file to encode
    if not args.message and not args.file:
        print("✗ Either --message or --file must be provided")
        return False

    if args.message and args.file:
        print("✗ Cannot specify both --message and --file")
        return False

    # Encode based on file type
    success = False

    if file_type == "image":
        success = encode_image(
            args.input, args.output, args.message, args.file
        )
    elif file_type == "audio":
        success = encode_audio(
            args.input, args.output, args.message, args.file
        )
    elif file_type == "text":
        method = (
            args.text_method if hasattr(args, "text_method") else "whitespace"
        )
        success = encode_text(
            args.input, args.output, args.message, args.file, method
        )

    return success


def decode_command(args: argparse.Namespace) -> bool:
    """Handle decode command

    Args:
        args: Parsed command line arguments

    Returns:
        True if decoding was successful, False otherwise
    """
    # Detect input file type
    file_type = detect_file_type(args.input)

    if file_type == "unknown":
        print(f"✗ Unsupported file format: {get_file_extension(args.input)}")
        print(
            "  Supported formats: PNG, JPEG (images), WAV (audio), TXT, MD (text)"
        )
        return False

    # Decode based on file type
    decoded_message: Optional[str] = None

    if file_type == "image":
        decoded_message = decode_image(args.input)
    elif file_type == "audio":
        decoded_message = decode_audio(args.input)
    elif file_type == "text":
        method = args.text_method if hasattr(args, "text_method") else "auto"
        decoded_message = decode_text(args.input, method)

    if decoded_message:
        print("\n" + "=" * 50)
        print("DECODED MESSAGE:")
        print("=" * 50)
        print(decoded_message)
        print("=" * 50)

        # Save to file if requested
        if args.output:
            try:
                output_path = Path(args.output)
                output_path.write_text(decoded_message, encoding="utf-8")
                print(f"✓ Decoded message saved to {args.output}")
            except (OSError, IOError, UnicodeError) as e:
                print(f"✗ Failed to save decoded message: {str(e)}")

        return True
    return False


def capacity_command(args: argparse.Namespace) -> bool:
    """Handle capacity command

    Args:
        args: Parsed command line arguments

    Returns:
        True if capacity check was successful, False otherwise
    """
    file_type = detect_file_type(args.input)

    if file_type == "image":
        capacity = get_image_capacity(args.input)
        print(f"Image capacity: {capacity} characters")
    elif file_type == "audio":
        capacity = get_audio_capacity(args.input)
        print(f"Audio capacity: {capacity} characters")
    elif file_type == "text":
        print("Text steganography capacity depends on the cover text length")
        print("Use the encode command to test if your message fits")
    else:
        print(f"✗ Unsupported file format: {get_file_extension(args.input)}")
        return False

    return True


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="stegano-sec: Python-based offline steganography toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encode text message in image
  python stegano_sec.py encode -i input.png -o output.png -m "Secret message"

  # Encode file contents in image
  python stegano_sec.py encode -i input.png -o output.png -f secret.txt

  # Decode message from image
  python stegano_sec.py decode -i encoded.png

  # Decode and save to file
  python stegano_sec.py decode -i encoded.png -o decoded.txt

  # Check capacity of image
  python stegano_sec.py capacity -i image.png

  # Encode in WAV audio
  python stegano_sec.py encode -i input.wav -o output.wav -m "Secret"

  # Encode in text with zero-width characters
  python stegano_sec.py encode -i cover.txt -o encoded.txt -m "Secret" \\
      --text-method zero_width

Supported formats:
  Images: PNG, JPEG (LSB steganography)
  Audio:  WAV (LSB steganography)
  Text:   TXT, MD (whitespace or zero-width character encoding)
        """,
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )

    # Encode command
    encode_parser = subparsers.add_parser(
        "encode", help="Encode message into media file"
    )
    encode_parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input media file (image/audio/text)",
    )
    encode_parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output file with encoded message",
    )

    # Message source (mutually exclusive)
    message_group = encode_parser.add_mutually_exclusive_group(required=True)
    message_group.add_argument(
        "-m", "--message", help="Text message to encode"
    )
    message_group.add_argument(
        "-f", "--file", help="File containing message to encode"
    )

    encode_parser.add_argument(
        "--text-method",
        choices=["whitespace", "zero_width"],
        default="whitespace",
        help="Method for text steganography (default: whitespace)",
    )

    # Decode command
    decode_parser = subparsers.add_parser(
        "decode", help="Decode message from media file"
    )
    decode_parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input media file with hidden message",
    )
    decode_parser.add_argument(
        "-o", "--output", help="Output file to save decoded message"
    )
    decode_parser.add_argument(
        "--text-method",
        choices=["whitespace", "zero_width", "auto"],
        default="auto",
        help="Method for text steganography (default: auto)",
    )

    # Capacity command
    capacity_parser = subparsers.add_parser(
        "capacity", help="Check media file capacity"
    )
    capacity_parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Input media file to check capacity",
    )

    return parser


def main() -> int:
    """Main entry point

    Returns:
        Exit code: 0 for success, 1 for failure
    """
    parser = create_parser()

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    args = parser.parse_args()

    # Handle commands
    success = False

    try:
        if args.command == "encode":
            success = encode_command(args)
        elif args.command == "decode":
            success = decode_command(args)
        elif args.command == "capacity":
            success = capacity_command(args)
        else:
            parser.print_help()
            return 1

    except (KeyboardInterrupt, SystemExit):
        print("\n✗ Operation cancelled by user")
        return 1
    except (OSError, ValueError, ImportError) as e:
        print(f"✗ Unexpected error: {str(e)}")
        return 1

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
