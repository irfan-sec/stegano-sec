# Changelog

## [3.0.0] - 2026-02-26

### New Features
- **🔒 AES-256 Encryption**: Optional password-based encryption for hidden messages using Fernet (AES-128-CBC + HMAC-SHA256) with PBKDF2 key derivation (600,000 iterations)
- **🖼️ BMP Image Support**: Added BMP format support for image steganography
- **📋 Version Flag**: Added `-V`/`--version` CLI flag to display current version
- **🔐 Crypto Module**: New `stegano/crypto.py` module with `encrypt_message()`, `decrypt_message()`, and `is_encrypted()` functions

### CLI Enhancements
- **`-p`/`--password`**: New flag for encode and decode commands to enable AES-256 encryption/decryption
- Automatic detection of encrypted messages during decoding with clear user prompts

### GUI Enhancements
- **Password fields**: Added encryption password input to both Encode and Decode tabs
- **BMP support**: Updated file dialogs to include BMP format

### Dependencies
- **Added**: `cryptography>=42.0.4` for AES-256 encryption support

### Testing
- **6 new tests**: Encryption/decryption cycles, wrong password handling, BMP format support, encrypted steganography end-to-end test
- **11 total tests** all passing

### Backwards Compatibility
- **✅ Fully backwards compatible**: All existing functionality works unchanged
- Messages encoded without password can still be decoded without password
- Encrypted messages are clearly identified with the `STEGENC1:` prefix

## [2.0.1] - 2024-09-28

### Maintenance
- **🐛 Code Quality**: Confirmed pylint compliance (10.00/10 rating maintained)
- **🏷️ Version Bump**: Updated version to 2.0.1 for maintenance release
- **✅ Testing**: All existing tests continue to pass

## [2.0.0] - 2024-09-06

### Major Upgrades
- **🔄 Modernized Python Package**: Added `pyproject.toml` configuration for modern Python packaging standards
- **🎯 Type Safety**: Added comprehensive type hints throughout the codebase for better IDE support and error detection
- **📁 Path Handling**: Migrated from `os.path` to modern `pathlib.Path` for better file handling
- **🧹 Dependency Cleanup**: Removed unnecessary `argparse` dependency (built into Python 3.2+)
- **📦 Development Tools**: Added comprehensive development dependencies and configuration

### New Features
- **✅ Test Suite**: Added pytest-based test framework with basic functionality tests
- **🔧 Development Setup**: Added pre-commit hooks configuration for code quality
- **📝 Enhanced Documentation**: Improved function documentation with proper type annotations
- **🛠️ Package Installation**: Tool can now be installed as a proper Python package

### Code Quality Improvements
- **Type Hints**: Full type annotation coverage across all modules
- **Modern Python**: Leverages Python 3.8+ features and best practices  
- **Better Error Handling**: Improved exception handling with clearer error messages
- **Code Formatting**: Configured Black, isort, flake8, and mypy for consistent code style

### Development Environment
- **📋 Requirements**: Split development dependencies into `requirements-dev.txt`
- **🔍 Linting**: Pre-configured linting tools (flake8, black, isort, mypy)
- **🧪 Testing**: Basic test suite with pytest configuration
- **🔒 Security**: Optional security scanning tools (bandit, safety)

### Backwards Compatibility
- **✅ CLI Interface**: All existing command-line functionality preserved
- **✅ API Compatibility**: All public APIs remain unchanged
- **✅ File Formats**: All supported formats (PNG, JPEG, WAV, TXT) continue to work

## [1.0.0] - Previous Version

### Initial Features
- LSB steganography for images (PNG, JPEG)
- LSB steganography for audio (WAV)  
- Text steganography with whitespace and zero-width characters
- Command-line interface
- Basic utility functions