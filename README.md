# stegano-sec

**stegano-sec** is a Python-based, offline steganography toolkit for security enthusiasts, CTF players, and researchers. It allows you to hide (encode) and extract (decode) text or files within various media types—such as images (PNG, JPEG), audio (WAV), and plain text files—with no need for external APIs or internet access. The toolkit is designed to be modular, user-friendly, and easily extensible, making it ideal for both educational and practical infosec use.

> **🆕 Version 2.0.0**: Now with modern Python packaging, type hints, comprehensive testing, and improved development tools!

---

## Features

- **Encode and decode messages/files** in:
  - PNG & JPEG images (using LSB steganography)
  - WAV audio files (LSB steganography)
  - Plain text files (whitespace or zero-width character encoding)
- **Graphical User Interface (GUI)** - Easy-to-use tkinter-based interface
- **Command-line interface (CLI)** for easy usage and scripting
- **Modular codebase** for adding new media formats or encoding techniques
- **Offline & privacy-friendly**: No data ever leaves your computer
- **Modern Python**: Full type hints, pathlib usage, and Python 3.8+ compatibility
- **Developer-friendly**: Comprehensive test suite, pre-commit hooks, and linting tools
- **Pip installable**: Can be installed as a proper Python package

---

## Installation

### Quick Start
```bash
git clone https://github.com/irfan-sec/stegano-sec.git
cd stegano-sec
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Development Setup
```bash
git clone https://github.com/irfan-sec/stegano-sec.git
cd stegano-sec
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Optional: for development tools
```

### Package Installation (Future)
```bash
# Coming soon: pip install stegano-sec
pip install -e .  # Install in development mode
```

---

## Usage

### GUI (Graphical User Interface)

Launch the user-friendly GUI:

```bash
python stegano_sec_gui.py
```

The GUI provides three tabs:
- **Encode**: Hide messages in images, audio, or text files
- **Decode**: Extract hidden messages from files
- **Capacity**: Check how much data a file can hide

![stegano-sec GUI](https://github.com/user-attachments/assets/7aa045d4-a56c-4b8b-9609-655abf9cca2b)

### CLI (Command Line Interface)

#### Encode a message in an image

```bash
python stegano_sec.py encode -i input.png -o output.png -m "Secret message here"
```

#### Decode a message from an image

```bash
python stegano_sec.py decode -i output.png
```

#### Encode a file in a WAV audio

```bash
python stegano_sec.py encode -i input.wav -o output.wav -f secret.txt
```

#### More options

See all available commands and options:

```bash
python stegano_sec.py --help
```

---

## Project Structure

```
stegano-sec/
├── stegano_sec.py         # CLI entry point
├── stegano_sec_gui.py     # GUI entry point
├── stegano/
│   ├── __init__.py
│   ├── image.py           # Image steganography functions
│   ├── audio.py           # Audio steganography functions
│   ├── text.py            # Text steganography functions
│   └── utils.py           # Helper utilities
├── requirements.txt
├── README.md
└── examples/
    └── sample.png
```

---

## Development

### Running Tests
```bash
# Run basic test suite
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v
```

### Code Quality Tools
```bash
# Format code with Black
black stegano/ stegano_sec.py tests/

# Sort imports with isort
isort stegano/ stegano_sec.py tests/

# Lint with flake8
flake8 stegano/ stegano_sec.py tests/

# Type checking with mypy
mypy stegano/ stegano_sec.py
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks (optional)
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

---

## What's New in v2.0.0

- **🔧 Modern Python Packaging**: Added `pyproject.toml` with comprehensive project metadata
- **🎯 Type Safety**: Full type hints across all modules for better IDE support
- **📁 Path Handling**: Migrated from `os.path` to modern `pathlib.Path`
- **✅ Testing**: Added pytest-based test suite with basic functionality tests
- **🛠️ Development Tools**: Pre-commit hooks, linting, formatting, and type checking
- **📦 Package Installation**: Can now be installed as a proper Python package
- **🧹 Dependency Cleanup**: Removed unnecessary dependencies (argparse)
- **📝 Better Documentation**: Enhanced docstrings and type annotations

All existing functionality remains fully compatible!

---

## Security Notice

This toolkit is for educational and research purposes. Steganography can hide information but does **not** encrypt it. Do not rely on it for strong security or privacy in adversarial environments.

---

## Contributing

Pull requests, bug reports, and feature suggestions are welcome! Please open an issue or submit a PR.

---

## License

MIT License

---

## Credits

Developed by [@irfan-sec](https://github.com/irfan-sec)
