"""
Audio steganography module using LSB (Least Significant Bit) encoding
Supports WAV audio format
"""

import wave
import numpy as np
from .utils import (
    validate_file_exists, validate_output_path,
    string_to_binary, binary_to_string,
    add_delimiter, find_delimiter,
    is_valid_audio_format
)


def encode_audio(input_path, output_path, message, file_path=None):
    """
    Encode a message or file content into a WAV audio file using LSB steganography

    Args:
        input_path (str): Path to input WAV file
        output_path (str): Path to save encoded WAV file
        message (str): Text message to hide (if file_path is None)
        file_path (str): Path to file whose content should be hidden

    Returns:
        bool: True if encoding successful

    Raises:
        FileNotFoundError: If input files don't exist
        ValueError: If message too long for audio capacity or invalid format
        Exception: For other encoding errors
    """
    try:
        # Validate inputs
        validate_file_exists(input_path)
        validate_output_path(output_path)

        if not is_valid_audio_format(input_path):
            raise ValueError("Input must be a WAV audio file")

        # Read message from file if file_path provided
        if file_path:
            validate_file_exists(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                message = f.read()

        if not message:
            raise ValueError("Message cannot be empty")

        # Open WAV file and read audio data
        with wave.open(input_path, 'rb') as wav_in:
            # Get audio parameters
            frames = wav_in.getnframes()
            sample_width = wav_in.getsampwidth()
            framerate = wav_in.getframerate()
            channels = wav_in.getnchannels()

            print(f"Audio info: {frames} frames, {sample_width} bytes/sample, {channels} channels, {framerate} Hz")

            # Read all audio data
            audio_data = wav_in.readframes(frames)

        # Convert to numpy array based on sample width
        if sample_width == 1:
            # 8-bit samples (unsigned)
            audio_array = np.frombuffer(audio_data, dtype=np.uint8)
        elif sample_width == 2:
            # 16-bit samples (signed)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
        elif sample_width == 4:
            # 32-bit samples (signed)
            audio_array = np.frombuffer(audio_data, dtype=np.int32)
        else:
            raise ValueError(f"Unsupported sample width: {sample_width} bytes")

        # Check capacity (1 bit per sample)
        max_chars = (len(audio_array) // 8) - 2  # Reserve space for delimiter
        if len(message) > max_chars:
            raise ValueError(f"Message too long. Maximum capacity: {max_chars} characters, got: {len(message)}")

        # Convert message to binary with delimiter
        binary_message = add_delimiter(string_to_binary(message))

        # Create a copy of audio data for modification
        modified_audio = audio_array.copy()

        # Encode message into LSBs
        for i, bit in enumerate(binary_message):
            if i < len(modified_audio):
                # Clear LSB and set new bit
                if sample_width == 1:  # Unsigned 8-bit
                    modified_audio[i] = (modified_audio[i] & 0xFE) | int(bit)
                else:  # Signed 16-bit or 32-bit
                    # For signed integers, we need to be careful with the LSB
                    modified_audio[i] = (modified_audio[i] & ~1) | int(bit)

        # Write encoded audio to output file
        with wave.open(output_path, 'wb') as wav_out:
            wav_out.setnchannels(channels)
            wav_out.setsampwidth(sample_width)
            wav_out.setframerate(framerate)
            wav_out.writeframes(modified_audio.tobytes())

        print(f"✓ Message successfully encoded into {output_path}")
        print(f"  Hidden message length: {len(message)} characters")
        print(f"  Audio capacity: {max_chars} characters")

        return True

    except Exception as e:
        print(f"✗ Encoding failed: {str(e)}")
        return False


def decode_audio(input_path):
    """
    Decode hidden message from a WAV audio file using LSB steganography

    Args:
        input_path (str): Path to WAV file with hidden message

    Returns:
        str: Decoded message or None if decoding failed

    Raises:
        FileNotFoundError: If input file doesn't exist
        Exception: For other decoding errors
    """
    try:
        # Validate inputs
        validate_file_exists(input_path)

        if not is_valid_audio_format(input_path):
            raise ValueError("Input must be a WAV audio file")

        # Open WAV file and read audio data
        with wave.open(input_path, 'rb') as wav_in:
            frames = wav_in.getnframes()
            sample_width = wav_in.getsampwidth()
            audio_data = wav_in.readframes(frames)

        # Convert to numpy array based on sample width
        if sample_width == 1:
            audio_array = np.frombuffer(audio_data, dtype=np.uint8)
        elif sample_width == 2:
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
        elif sample_width == 4:
            audio_array = np.frombuffer(audio_data, dtype=np.int32)
        else:
            raise ValueError(f"Unsupported sample width: {sample_width} bytes")

        # Extract LSBs to get binary message
        binary_message = ''
        for sample in audio_array:
            binary_message += str(sample & 1)  # Get LSB

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


def get_audio_capacity(audio_path):
    """
    Get the maximum message capacity for a WAV audio file

    Args:
        audio_path (str): Path to WAV audio file

    Returns:
        int: Maximum number of characters that can be hidden
    """
    try:
        validate_file_exists(audio_path)

        if not is_valid_audio_format(audio_path):
            raise ValueError("Input must be a WAV audio file")

        with wave.open(audio_path, 'rb') as wav_in:
            frames = wav_in.getnframes()

        # 1 bit per sample, 8 bits per character, minus space for delimiter
        return (frames // 8) - 2

    except Exception as e:
        print(f"✗ Failed to calculate capacity: {str(e)}")
        return 0
