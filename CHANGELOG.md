# Changelog

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