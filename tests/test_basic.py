"""Basic smoke tests for stegano-sec functionality"""

# pylint: disable=duplicate-code  # Similar patterns expected

import os
import sys
import tempfile
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# pylint: disable=import-error,wrong-import-position
# pytest may not be available, imports after path mod
import pytest

from stegano import decode_image, encode_image
from stegano.crypto import decrypt_message, encrypt_message, is_encrypted
from stegano.utils import get_file_extension, validate_file_exists


class TestBasicFunctionality:
    """Test basic steganography functionality"""

    def test_image_encode_decode_cycle(self):
        """Test that we can encode and decode a message in an image"""
        # Use the existing sample image
        sample_image = Path(__file__).parent.parent / "examples" / "sample.png"

        if not sample_image.exists():
            pytest.skip("Sample image not found")

        test_message = "This is a test message for steganography!"

        with tempfile.NamedTemporaryFile(
            suffix=".png", delete=False
        ) as tmp_file:
            try:
                # Test encoding
                success = encode_image(
                    str(sample_image), tmp_file.name, test_message, None
                )
                assert success, "Encoding should succeed"

                # Test decoding
                decoded_message = decode_image(tmp_file.name)
                assert (
                    decoded_message is not None
                ), "Decoding should return a message"
                assert (
                    decoded_message == test_message
                ), "Decoded message should match original"

            finally:
                # Clean up
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)

    def test_utils_validate_file_exists(self):
        """Test file validation utility"""
        # Test with existing file
        sample_image = Path(__file__).parent.parent / "examples" / "sample.png"
        if sample_image.exists():
            assert validate_file_exists(str(sample_image))

        # Test with non-existent file
        with pytest.raises(FileNotFoundError):
            validate_file_exists("non_existent_file.png")

    def test_utils_get_file_extension(self):
        """Test file extension utility"""
        assert get_file_extension("test.png") == ".png"
        assert get_file_extension("TEST.PNG") == ".png"
        assert get_file_extension("file.jpg") == ".jpg"
        assert get_file_extension("file.jpeg") == ".jpeg"
        assert get_file_extension("file.wav") == ".wav"
        assert get_file_extension("file") == ""


class TestVersionInfo:
    """Test version and package information"""

    def test_version_import(self):
        """Test that version can be imported"""
        # pylint: disable=import-outside-toplevel  # Version import only needed in test
        from stegano import __version__

        assert __version__ == "3.0.0"

    def test_package_imports(self):
        """Test that main functions can be imported"""
        # These functions are already imported at module level, just check they work
        # pylint: disable=redefined-outer-name  # Testing imported functions
        assert callable(encode_image)
        assert callable(decode_image)

        # Import audio and text functions for testing
        # pylint: disable=import-outside-toplevel  # Only needed in this test
        from stegano import (
            decode_audio,
            decode_text,
            encode_audio,
            encode_text,
            encrypt_message,
            decrypt_message,
            is_encrypted,
        )

        assert callable(encode_audio)
        assert callable(decode_audio)
        assert callable(encode_text)
        assert callable(decode_text)
        assert callable(encrypt_message)
        assert callable(decrypt_message)
        assert callable(is_encrypted)


class TestEncryption:
    """Test encryption and decryption functionality"""

    def test_encrypt_decrypt_cycle(self):
        """Test that encrypting and decrypting a message returns the original"""
        message = "This is a secret message!"
        password = "testpassword123"

        encrypted = encrypt_message(message, password)
        assert encrypted != message
        assert is_encrypted(encrypted)

        decrypted = decrypt_message(encrypted, password)
        assert decrypted == message

    def test_wrong_password_returns_none(self):
        """Test that decrypting with wrong password returns None"""
        message = "Secret data"
        encrypted = encrypt_message(message, "correct_password")

        result = decrypt_message(encrypted, "wrong_password")
        assert result is None

    def test_unencrypted_message_passthrough(self):
        """Test that non-encrypted messages pass through decrypt unchanged"""
        message = "Plain text message"
        result = decrypt_message(message, "any_password")
        assert result == message

    def test_is_encrypted_detection(self):
        """Test encrypted message detection"""
        encrypted = encrypt_message("test", "pass")
        assert is_encrypted(encrypted)
        assert not is_encrypted("regular text")

    def test_encrypted_image_encode_decode(self):
        """Test encoding and decoding an encrypted message in an image"""
        sample_image = Path(__file__).parent.parent / "examples" / "sample.png"

        if not sample_image.exists():
            pytest.skip("Sample image not found")

        test_message = "Encrypted steganography test!"
        password = "my_secure_password"

        # Encrypt and encode
        encrypted_msg = encrypt_message(test_message, password)

        with tempfile.NamedTemporaryFile(
            suffix=".png", delete=False
        ) as tmp_file:
            try:
                success = encode_image(
                    str(sample_image), tmp_file.name, encrypted_msg, None
                )
                assert success, "Encoding should succeed"

                # Decode and decrypt
                decoded = decode_image(tmp_file.name)
                assert decoded is not None
                assert is_encrypted(decoded)

                decrypted = decrypt_message(decoded, password)
                assert decrypted == test_message

            finally:
                if os.path.exists(tmp_file.name):
                    os.unlink(tmp_file.name)

    def test_bmp_format_support(self):
        """Test that BMP format is recognized as valid"""
        from stegano.utils import is_valid_image_format

        assert is_valid_image_format("test.bmp")
        assert is_valid_image_format("test.png")
        assert is_valid_image_format("test.jpg")
        assert not is_valid_image_format("test.gif")
