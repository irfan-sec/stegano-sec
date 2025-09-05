# stegano-sec

**stegano-sec** is a Python-based, offline steganography toolkit for security enthusiasts, CTF players, and researchers. It allows you to hide (encode) and extract (decode) text or files within various media types—such as images (PNG, JPEG), audio (WAV), and plain text files—with no need for external APIs or internet access. The toolkit is designed to be modular, user-friendly, and easily extensible, making it ideal for both educational and practical infosec use.

---

## Features

- **Encode and decode messages/files** in:
  - PNG & JPEG images (using LSB steganography)
  - WAV audio files (LSB steganography)
  - Plain text files (whitespace or zero-width character encoding)
- **Command-line interface (CLI)** for easy usage and scripting
- **Modular codebase** for adding new media formats or encoding techniques
- **Offline & privacy-friendly**: No data ever leaves your computer
- **Optional GUI** for non-CLI users (planned)
- **Comprehensive documentation** and usage examples

---

## Installation

```bash
git clone https://github.com/irfan-sec/stegano-sec.git
cd stegano-sec
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Encode a message in an image

```bash
python stegano_sec.py encode -i input.png -o output.png -m "Secret message here"
```

### Decode a message from an image

```bash
python stegano_sec.py decode -i output.png
```

### Encode a file in a WAV audio

```bash
python stegano_sec.py encode -i input.wav -o output.wav -f secret.txt
```

### More options

See all available commands and options:

```bash
python stegano_sec.py --help
```

---

## Project Structure

```
stegano-sec/
├── stegano_sec.py         # CLI entry point
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
