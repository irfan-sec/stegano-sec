"""
Audio steganography module using LSB (Least Significant Bit) encoding
Supports WAV audio format
"""

import wave
from pathlib import Path
from typing import Dict, Any, Optional, Union, Tuple

# pylint: disable=import-error  # numpy may not be available
import numpy as np

from .utils import (
    add_delimiter,
    decode_binary_message,
    is_valid_audio_format,
    prepare_message_from_file,
    string_to_binary,
    validate_file_exists,
    validate_output_path,
)


def _load_wav_data(input_path: Union[str, Path]) -> Tuple[Dict[str, Any], bytes]:
    """Load WAV file data and return audio parameters and data."""
    with wave.open(str(input_path), "rb") as wav_in:
        # Get audio parameters
        params = {
            "frames": wav_in.getnframes(),
            "sample_width": wav_in.getsampwidth(),
            "framerate": wav_in.getframerate(),
            "channels": wav_in.getnchannels(),
        }

        print(
            f"Audio info: {params['frames']} frames, {params['sample_width']} bytes/sample, "
            f"{params['channels']} channels, {params['framerate']} Hz"
        )

        # Read all audio data
        audio_data = wav_in.readframes(params["frames"])

    return params, audio_data


def _convert_audio_to_array(audio_data: bytes, sample_width: int) -> Any:
    """Convert audio data to numpy array based on sample width."""
    if sample_width == 1:
        return np.frombuffer(audio_data, dtype=np.uint8)
    if sample_width == 2:
        return np.frombuffer(audio_data, dtype=np.int16)
    if sample_width == 4:
        return np.frombuffer(audio_data, dtype=np.int32)

    raise ValueError(f"Unsupported sample width: {sample_width} bytes")


def encode_audio(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    message: Optional[str],
    file_path: Optional[Union[str, Path]] = None,
) -> bool:
    """
    Encode a message or file content into a WAV audio file using LSB
    steganography

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

        # Prepare message
        message = prepare_message_from_file(message, file_path)

        # Load WAV data
        params, audio_data = _load_wav_data(input_path)

        # Convert to numpy array
        audio_array = _convert_audio_to_array(
            audio_data, params["sample_width"]
        )

        # Check capacity and encode
        max_chars = (len(audio_array) // 8) - 2
        if len(message) > max_chars:
            raise ValueError(
                f"Message too long. Maximum capacity: {max_chars} characters, "
                f"got: {len(message)}"
            )

        # Convert message to binary and encode
        binary_message = add_delimiter(string_to_binary(message))
        modified_audio = audio_array.copy()

        # Encode message into LSBs
        for i, bit in enumerate(binary_message):
            if i < len(modified_audio):
                if params["sample_width"] == 1:
                    modified_audio[i] = (modified_audio[i] & 0xFE) | int(bit)
                else:
                    modified_audio[i] = (modified_audio[i] & ~1) | int(bit)

        # Write encoded audio to output file
        with wave.open(str(output_path), "wb") as wav_out:
            # pylint: disable=no-member  # wav_out is Wave_write, not Wave_read
            wav_out.setnchannels(params["channels"])
            wav_out.setsampwidth(params["sample_width"])
            wav_out.setframerate(params["framerate"])
            wav_out.writeframes(modified_audio.tobytes())

        print(f"✓ Message successfully encoded into {output_path}")
        print(f"  Hidden message length: {len(message)} characters")
        print(f"  Audio capacity: {max_chars} characters")

        return True

    except (OSError, ValueError, AttributeError, TypeError) as e:
        print(f"✗ Encoding failed: {str(e)}")
        return False


def decode_audio(input_path: Union[str, Path]) -> Optional[str]:
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
        with wave.open(str(input_path), "rb") as wav_in:
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
        binary_message = ""
        for sample in audio_array:
            binary_message += str(sample & 1)  # Get LSB

        # Find delimiter and extract message
        return decode_binary_message(binary_message, input_path)

    except (OSError, ValueError, AttributeError, TypeError) as e:
        print(f"✗ Decoding failed: {str(e)}")
        return None


def get_audio_capacity(audio_path: Union[str, Path]) -> int:
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

        with wave.open(str(audio_path), "rb") as wav_in:
            frames = wav_in.getnframes()

        # 1 bit per sample, 8 bits per character, minus space for delimiter
        return (frames // 8) - 2

    except (OSError, AttributeError, ValueError) as e:
        print(f"✗ Failed to calculate capacity: {str(e)}")
        return 0
