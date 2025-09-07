"""
Image steganography module using LSB (Least Significant Bit) encoding
Supports PNG and JPEG formats
"""

# pylint: disable=import-error  # PIL and numpy may not be available in all environments
from PIL import Image
import numpy as np
from .utils import (
    validate_file_exists, validate_output_path,
    string_to_binary, add_delimiter,
    is_valid_image_format, calculate_capacity, prepare_message_from_file, decode_binary_message
)


def _load_and_process_image(input_path):
    """Load image and convert to RGB array."""
    img = Image.open(input_path)

    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Convert image to numpy array
    img_array = np.array(img)
    return img_array, img_array.shape


def encode_image(input_path, output_path, message, file_path=None):
    """
    Encode a message or file content into an image using LSB steganography

    Args:
        input_path (str): Path to input image
        output_path (str): Path to save encoded image
        message (str): Text message to hide (if file_path is None)
        file_path (str): Path to file whose content should be hidden

    Returns:
        bool: True if encoding successful

    Raises:
        FileNotFoundError: If input files don't exist
        ValueError: If message too long for image capacity
        Exception: For other encoding errors
    """
    try:
        # Validate inputs
        validate_file_exists(input_path)
        validate_output_path(output_path)

        if not is_valid_image_format(input_path):
            raise ValueError("Input must be a PNG or JPEG image")

        # Prepare message and load image data
        message = prepare_message_from_file(message, file_path)
        img_array, shape = _load_and_process_image(input_path)

        # Check capacity and prepare for encoding
        max_chars = calculate_capacity(shape[1], shape[0], shape[2])
        if len(message) > max_chars:
            raise ValueError(f"Message too long. Maximum capacity: {max_chars} characters, "
                             f"got: {len(message)}")

        # Encode message into flattened array
        flat_array = img_array.flatten()
        for i, bit in enumerate(add_delimiter(string_to_binary(message))):
            if i < len(flat_array):
                flat_array[i] = (flat_array[i] & 0xFE) | int(bit)

        # Save encoded image
        # pylint: disable=too-many-function-args  # numpy reshape accepts multiple args
        Image.fromarray(
            flat_array.reshape(shape).astype(np.uint8)
        ).save(output_path, quality=95)

        print(f"✓ Message successfully encoded into {output_path}")
        print(f"  Hidden message length: {len(message)} characters")
        print(f"  Image capacity: {max_chars} characters")

        return True

    except (OSError, ValueError, AttributeError, TypeError) as e:
        print(f"✗ Encoding failed: {str(e)}")
        return False


def decode_image(input_path):
    """
    Decode hidden message from an image using LSB steganography

    Args:
        input_path (str): Path to image with hidden message

    Returns:
        str: Decoded message or None if decoding failed

    Raises:
        FileNotFoundError: If input file doesn't exist
        Exception: For other decoding errors
    """
    try:
        # Validate inputs
        validate_file_exists(input_path)

        if not is_valid_image_format(input_path):
            raise ValueError("Input must be a PNG or JPEG image")

        # Load image
        img = Image.open(input_path)

        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Convert to numpy array
        img_array = np.array(img)

        # Flatten array
        flat_array = img_array.flatten()

        # Extract LSBs to get binary message
        binary_message = ''
        for pixel_value in flat_array:
            binary_message += str(pixel_value & 1)  # Get LSB

        # Find delimiter and extract message
        return decode_binary_message(binary_message, input_path)

    except (OSError, ValueError, AttributeError, TypeError) as e:
        print(f"✗ Decoding failed: {str(e)}")
        return None


def get_image_capacity(image_path):
    """
    Get the maximum message capacity for an image

    Args:
        image_path (str): Path to image file

    Returns:
        int: Maximum number of characters that can be hidden
    """
    try:
        validate_file_exists(image_path)

        if not is_valid_image_format(image_path):
            raise ValueError("Input must be a PNG or JPEG image")

        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        width, height = img.size
        return calculate_capacity(width, height, 3)

    except (OSError, AttributeError, ValueError) as e:
        print(f"✗ Failed to calculate capacity: {str(e)}")
        return 0
