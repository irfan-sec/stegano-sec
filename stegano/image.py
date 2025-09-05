"""
Image steganography module using LSB (Least Significant Bit) encoding
Supports PNG and JPEG formats
"""

from PIL import Image
import numpy as np
from .utils import (
    validate_file_exists, validate_output_path, 
    string_to_binary, binary_to_string,
    add_delimiter, find_delimiter,
    is_valid_image_format, calculate_capacity
)


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
            
        # Read message from file if file_path provided
        if file_path:
            validate_file_exists(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                message = f.read()
        
        if not message:
            raise ValueError("Message cannot be empty")
            
        # Load image
        img = Image.open(input_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Convert image to numpy array for easier manipulation
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Check capacity
        max_chars = calculate_capacity(width, height, channels)
        if len(message) > max_chars:
            raise ValueError(f"Message too long. Maximum capacity: {max_chars} characters, got: {len(message)}")
            
        # Convert message to binary with delimiter
        binary_message = add_delimiter(string_to_binary(message))
        
        # Flatten image array for easier bit manipulation
        flat_array = img_array.flatten()
        
        # Encode message into LSBs
        for i, bit in enumerate(binary_message):
            if i < len(flat_array):
                # Clear LSB and set new bit
                flat_array[i] = (flat_array[i] & 0xFE) | int(bit)
        
        # Reshape back to original dimensions
        encoded_array = flat_array.reshape(height, width, channels)
        
        # Convert back to PIL Image and save
        encoded_img = Image.fromarray(encoded_array.astype(np.uint8))
        encoded_img.save(output_path, quality=95)  # High quality for JPEG
        
        print(f"✓ Message successfully encoded into {output_path}")
        print(f"  Hidden message length: {len(message)} characters")
        print(f"  Image capacity: {max_chars} characters")
        
        return True
        
    except Exception as e:
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
            
        except Exception as e:
            print(f"✗ Failed to convert binary to text: {str(e)}")
            return None
            
    except Exception as e:
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
        
    except Exception as e:
        print(f"✗ Failed to calculate capacity: {str(e)}")
        return 0