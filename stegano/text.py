"""
Text steganography module using whitespace and zero-width character encoding
"""

import re
from .utils import validate_file_exists, validate_output_path


# Zero-width characters for steganography
ZERO_WIDTH_SPACE = '\u200B'          # Zero-width space
ZERO_WIDTH_NON_JOINER = '\u200C'     # Zero-width non-joiner
ZERO_WIDTH_JOINER = '\u200D'         # Zero-width joiner
WORD_JOINER = '\u2060'               # Word joiner

# Binary encoding using zero-width characters
ZERO_WIDTH_BINARY = {
    '00': ZERO_WIDTH_SPACE,
    '01': ZERO_WIDTH_NON_JOINER,
    '10': ZERO_WIDTH_JOINER,
    '11': WORD_JOINER
}

# Reverse mapping for decoding
BINARY_ZERO_WIDTH = {v: k for k, v in ZERO_WIDTH_BINARY.items()}


def encode_text_whitespace(cover_text, message):
    """
    Encode message using whitespace steganography
    Uses different numbers of spaces/tabs to represent binary data

    Args:
        cover_text (str): Text to hide message in
        message (str): Message to hide

    Returns:
        str: Cover text with hidden message
    """
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Delimiter

    # Split cover text into words
    words = cover_text.split()

    if len(binary_message) > len(words) - 1:
        raise ValueError(f"Message too long for cover text. Need {len(binary_message)} spaces, have {len(words) - 1}")

    # Build result with encoded spaces
    result = []
    binary_index = 0

    for i, word in enumerate(words):
        result.append(word)

        # Add space after word (except last word)
        if i < len(words) - 1:
            if binary_index < len(binary_message):
                # Use space count to encode binary
                bit = binary_message[binary_index]
                if bit == '0':
                    result.append(' ')      # Single space for 0
                else:
                    result.append('  ')     # Double space for 1
                binary_index += 1
            else:
                result.append(' ')          # Normal single space

    return ''.join(result)


def decode_text_whitespace(encoded_text):
    """
    Decode message from whitespace-encoded text

    Args:
        encoded_text (str): Text with hidden message

    Returns:
        str: Decoded message or None if not found
    """
    # Find spaces between words
    words = re.split(r'(\s+)', encoded_text)

    binary_message = ''

    # Extract binary from space patterns
    for i in range(1, len(words), 2):  # Every other element is whitespace
        space_sequence = words[i]
        if len(space_sequence) == 1:
            binary_message += '0'  # Single space = 0
        elif len(space_sequence) == 2:
            binary_message += '1'  # Double space = 1
        # Ignore other space patterns

    # Find delimiter
    delimiter = '1111111111111110'
    delimiter_pos = binary_message.find(delimiter)

    if delimiter_pos == -1:
        return None

    binary_message = binary_message[:delimiter_pos]

    # Convert binary to text
    try:
        chars = []
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))
        return ''.join(chars)
    except:
        return None


def encode_text_zero_width(cover_text, message):
    """
    Encode message using zero-width character steganography

    Args:
        cover_text (str): Text to hide message in
        message (str): Message to hide

    Returns:
        str: Cover text with hidden message using zero-width characters
    """
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Delimiter

    # Pad binary to make it divisible by 2 (for 2-bit encoding)
    if len(binary_message) % 2 != 0:
        binary_message += '0'

    # Split cover text into characters
    if len(binary_message) // 2 > len(cover_text):
        raise ValueError(f"Message too long for cover text. Need {len(binary_message) // 2} characters, have {len(cover_text)}")

    result = []
    binary_index = 0

    for char in cover_text:
        result.append(char)

        # Insert zero-width character after each character
        if binary_index < len(binary_message):
            # Take 2 bits and encode as zero-width character
            two_bits = binary_message[binary_index:binary_index + 2]
            if two_bits in ZERO_WIDTH_BINARY:
                result.append(ZERO_WIDTH_BINARY[two_bits])
            binary_index += 2

    return ''.join(result)


def decode_text_zero_width(encoded_text):
    """
    Decode message from zero-width character encoded text

    Args:
        encoded_text (str): Text with hidden zero-width characters

    Returns:
        str: Decoded message or None if not found
    """
    # Extract zero-width characters
    zero_width_chars = []
    for char in encoded_text:
        if char in BINARY_ZERO_WIDTH:
            zero_width_chars.append(char)

    if not zero_width_chars:
        return None

    # Convert zero-width characters back to binary
    binary_message = ''
    for char in zero_width_chars:
        binary_message += BINARY_ZERO_WIDTH[char]

    # Find delimiter
    delimiter = '1111111111111110'
    delimiter_pos = binary_message.find(delimiter)

    if delimiter_pos == -1:
        return None

    binary_message = binary_message[:delimiter_pos]

    # Convert binary to text
    try:
        chars = []
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))
        return ''.join(chars)
    except:
        return None


def encode_text(input_path, output_path, message, file_path=None, method='whitespace'):
    """
    Encode a message into a text file using specified steganography method

    Args:
        input_path (str): Path to input text file (cover text)
        output_path (str): Path to save encoded text file
        message (str): Text message to hide (if file_path is None)
        file_path (str): Path to file whose content should be hidden
        method (str): Encoding method ('whitespace' or 'zero_width')

    Returns:
        bool: True if encoding successful
    """
    try:
        # Validate inputs
        validate_file_exists(input_path)
        validate_output_path(output_path)

        # Read cover text
        with open(input_path, 'r', encoding='utf-8') as f:
            cover_text = f.read()

        if not cover_text.strip():
            raise ValueError("Cover text file is empty")

        # Read message from file if file_path provided
        if file_path:
            validate_file_exists(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                message = f.read()

        if not message:
            raise ValueError("Message cannot be empty")

        # Encode based on method
        if method == 'whitespace':
            encoded_text = encode_text_whitespace(cover_text, message)
        elif method == 'zero_width':
            encoded_text = encode_text_zero_width(cover_text, message)
        else:
            raise ValueError(f"Unknown encoding method: {method}")

        # Save encoded text
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encoded_text)

        print(f"✓ Message successfully encoded into {output_path}")
        print(f"  Encoding method: {method}")
        print(f"  Hidden message length: {len(message)} characters")

        return True

    except Exception as e:
        print(f"✗ Encoding failed: {str(e)}")
        return False


def decode_text(input_path, method='auto'):
    """
    Decode hidden message from a text file

    Args:
        input_path (str): Path to text file with hidden message
        method (str): Decoding method ('whitespace', 'zero_width', or 'auto')

    Returns:
        str: Decoded message or None if decoding failed
    """
    try:
        # Validate inputs
        validate_file_exists(input_path)

        # Read encoded text
        with open(input_path, 'r', encoding='utf-8') as f:
            encoded_text = f.read()

        if not encoded_text:
            raise ValueError("Input file is empty")

        decoded_message = None

        if method == 'auto' or method == 'whitespace':
            # Try whitespace decoding
            decoded_message = decode_text_whitespace(encoded_text)
            if decoded_message:
                print(f"✓ Message successfully decoded from {input_path} (whitespace method)")
                print(f"  Message length: {len(decoded_message)} characters")
                return decoded_message

        if method == 'auto' or method == 'zero_width':
            # Try zero-width character decoding
            decoded_message = decode_text_zero_width(encoded_text)
            if decoded_message:
                print(f"✓ Message successfully decoded from {input_path} (zero-width method)")
                print(f"  Message length: {len(decoded_message)} characters")
                return decoded_message

        if method != 'auto':
            print(f"✗ No hidden message found using {method} method")
        else:
            print("✗ No hidden message found using any method")

        return None

    except Exception as e:
        print(f"✗ Decoding failed: {str(e)}")
        return None
