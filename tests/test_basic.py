"""Basic smoke tests for stegano-sec functionality"""

import pytest
import tempfile
import os
from pathlib import Path

# Add the parent directory to Python path for imports
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stegano import encode_image, decode_image
from stegano.utils import validate_file_exists, get_file_extension


class TestBasicFunctionality:
    """Test basic steganography functionality"""
    
    def test_image_encode_decode_cycle(self):
        """Test that we can encode and decode a message in an image"""
        # Use the existing sample image
        sample_image = Path(__file__).parent.parent / "examples" / "sample.png"
        
        if not sample_image.exists():
            pytest.skip("Sample image not found")
        
        test_message = "This is a test message for steganography!"
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            try:
                # Test encoding
                success = encode_image(
                    str(sample_image), 
                    tmp_file.name, 
                    test_message, 
                    None
                )
                assert success, "Encoding should succeed"
                
                # Test decoding
                decoded_message = decode_image(tmp_file.name)
                assert decoded_message is not None, "Decoding should return a message"
                assert decoded_message == test_message, "Decoded message should match original"
                
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
        from stegano import __version__
        assert __version__ == "2.0.0"
    
    def test_package_imports(self):
        """Test that main functions can be imported"""
        from stegano import encode_image, decode_image
        from stegano import encode_audio, decode_audio  
        from stegano import encode_text, decode_text
        
        # Just test that they're callable
        assert callable(encode_image)
        assert callable(decode_image)
        assert callable(encode_audio) 
        assert callable(decode_audio)
        assert callable(encode_text)
        assert callable(decode_text)