#!/usr/bin/env python3
"""
stegano-sec GUI: Graphical User Interface for steganography toolkit

Provides a user-friendly tkinter-based GUI for encoding, decoding, and
checking capacity of steganography operations on images, audio, and text files.
"""

import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk
from typing import Optional

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import after path modification
# pylint: disable=wrong-import-position
# flake8: noqa: E402
from stegano import (
    decode_audio,
    decode_image,
    decode_text,
    encode_audio,
    encode_image,
    encode_text,
)
from stegano.audio import get_audio_capacity
from stegano.image import get_image_capacity
from stegano.utils import get_file_extension


class SteganoGUI:  # pylint: disable=too-many-instance-attributes
    """Main GUI class for stegano-sec"""

    def __init__(self, root: tk.Tk):
        """Initialize the GUI

        Args:
            root: The root tkinter window
        """
        self.root = root
        self.root.title("stegano-sec - Steganography Toolkit")
        self.root.geometry("800x600")

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.encode_tab = ttk.Frame(self.notebook)
        self.decode_tab = ttk.Frame(self.notebook)
        self.capacity_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.encode_tab, text="Encode")
        self.notebook.add(self.decode_tab, text="Decode")
        self.notebook.add(self.capacity_tab, text="Capacity")

        # Setup each tab
        self.setup_encode_tab()
        self.setup_decode_tab()
        self.setup_capacity_tab()

    def setup_encode_tab(self) -> None:
        """Setup the encode tab"""
        # Input file selection
        input_frame = ttk.LabelFrame(self.encode_tab, text="Input File", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.encode_input_path = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.encode_input_path, width=60).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            input_frame, text="Browse...", command=self.browse_encode_input
        ).pack(side=tk.LEFT)

        # Output file selection
        output_frame = ttk.LabelFrame(self.encode_tab, text="Output File", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=5)

        self.encode_output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.encode_output_path, width=60).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            output_frame, text="Browse...", command=self.browse_encode_output
        ).pack(side=tk.LEFT)

        # Message input
        message_frame = ttk.LabelFrame(self.encode_tab, text="Message", padding=10)
        message_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Radio buttons for message source
        self.encode_message_source = tk.StringVar(value="text")
        ttk.Radiobutton(
            message_frame,
            text="Enter text message",
            variable=self.encode_message_source,
            value="text",
            command=self.update_encode_message_widgets,
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            message_frame,
            text="Load message from file",
            variable=self.encode_message_source,
            value="file",
            command=self.update_encode_message_widgets,
        ).pack(anchor=tk.W)

        # Text message input
        self.encode_message_text = scrolledtext.ScrolledText(
            message_frame, height=8, width=70
        )
        self.encode_message_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # File message input
        file_msg_frame = ttk.Frame(message_frame)
        file_msg_frame.pack(fill=tk.X, pady=5)
        self.encode_message_file = tk.StringVar()
        self.encode_message_file_entry = ttk.Entry(
            file_msg_frame, textvariable=self.encode_message_file, width=50
        )
        self.encode_message_file_entry.pack(side=tk.LEFT, padx=5)
        self.encode_message_file_button = ttk.Button(
            file_msg_frame, text="Browse...", command=self.browse_encode_message_file
        )
        self.encode_message_file_button.pack(side=tk.LEFT)

        # Text method for text files
        text_method_frame = ttk.Frame(message_frame)
        text_method_frame.pack(fill=tk.X, pady=5)
        ttk.Label(text_method_frame, text="Text steganography method:").pack(
            side=tk.LEFT, padx=5
        )
        self.encode_text_method = tk.StringVar(value="whitespace")
        ttk.Radiobutton(
            text_method_frame,
            text="Whitespace",
            variable=self.encode_text_method,
            value="whitespace",
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            text_method_frame,
            text="Zero-width",
            variable=self.encode_text_method,
            value="zero_width",
        ).pack(side=tk.LEFT, padx=5)

        # Encode button
        ttk.Button(
            self.encode_tab, text="Encode Message", command=self.encode_message
        ).pack(pady=10)

        # Initial widget state
        self.update_encode_message_widgets()

    def setup_decode_tab(self) -> None:
        """Setup the decode tab"""
        # Input file selection
        input_frame = ttk.LabelFrame(self.decode_tab, text="Input File", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.decode_input_path = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.decode_input_path, width=60).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            input_frame, text="Browse...", command=self.browse_decode_input
        ).pack(side=tk.LEFT)

        # Output options
        output_frame = ttk.LabelFrame(
            self.decode_tab, text="Output Options (Optional)", padding=10
        )
        output_frame.pack(fill=tk.X, padx=10, pady=5)

        self.decode_save_to_file = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            output_frame,
            text="Save decoded message to file",
            variable=self.decode_save_to_file,
            command=self.update_decode_output_widgets,
        ).pack(anchor=tk.W)

        output_path_frame = ttk.Frame(output_frame)
        output_path_frame.pack(fill=tk.X, pady=5)
        self.decode_output_path = tk.StringVar()
        self.decode_output_entry = ttk.Entry(
            output_path_frame, textvariable=self.decode_output_path, width=50
        )
        self.decode_output_entry.pack(side=tk.LEFT, padx=5)
        self.decode_output_button = ttk.Button(
            output_path_frame, text="Browse...", command=self.browse_decode_output
        )
        self.decode_output_button.pack(side=tk.LEFT)

        # Text method for text files
        text_method_frame = ttk.Frame(output_frame)
        text_method_frame.pack(fill=tk.X, pady=5)
        ttk.Label(text_method_frame, text="Text steganography method:").pack(
            side=tk.LEFT, padx=5
        )
        self.decode_text_method = tk.StringVar(value="auto")
        ttk.Radiobutton(
            text_method_frame,
            text="Auto",
            variable=self.decode_text_method,
            value="auto",
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            text_method_frame,
            text="Whitespace",
            variable=self.decode_text_method,
            value="whitespace",
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            text_method_frame,
            text="Zero-width",
            variable=self.decode_text_method,
            value="zero_width",
        ).pack(side=tk.LEFT, padx=5)

        # Decoded message display
        result_frame = ttk.LabelFrame(
            self.decode_tab, text="Decoded Message", padding=10
        )
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.decode_result_text = scrolledtext.ScrolledText(
            result_frame, height=10, width=70
        )
        self.decode_result_text.pack(fill=tk.BOTH, expand=True)

        # Decode button
        ttk.Button(
            self.decode_tab, text="Decode Message", command=self.decode_message
        ).pack(pady=10)

        # Initial widget state
        self.update_decode_output_widgets()

    def setup_capacity_tab(self) -> None:
        """Setup the capacity tab"""
        # Input file selection
        input_frame = ttk.LabelFrame(self.capacity_tab, text="Input File", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.capacity_input_path = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.capacity_input_path, width=60).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(
            input_frame, text="Browse...", command=self.browse_capacity_input
        ).pack(side=tk.LEFT)

        # Result display
        result_frame = ttk.LabelFrame(
            self.capacity_tab, text="Capacity Information", padding=10
        )
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.capacity_result_text = scrolledtext.ScrolledText(
            result_frame, height=10, width=70
        )
        self.capacity_result_text.pack(fill=tk.BOTH, expand=True)

        # Check capacity button
        ttk.Button(
            self.capacity_tab, text="Check Capacity", command=self.check_capacity
        ).pack(pady=10)

    def update_encode_message_widgets(self) -> None:
        """Update encode message widgets based on selection"""
        if self.encode_message_source.get() == "text":
            self.encode_message_text.config(state=tk.NORMAL)
            self.encode_message_file_entry.config(state=tk.DISABLED)
            self.encode_message_file_button.config(state=tk.DISABLED)
        else:
            self.encode_message_text.config(state=tk.DISABLED)
            self.encode_message_file_entry.config(state=tk.NORMAL)
            self.encode_message_file_button.config(state=tk.NORMAL)

    def update_decode_output_widgets(self) -> None:
        """Update decode output widgets based on selection"""
        if self.decode_save_to_file.get():
            self.decode_output_entry.config(state=tk.NORMAL)
            self.decode_output_button.config(state=tk.NORMAL)
        else:
            self.decode_output_entry.config(state=tk.DISABLED)
            self.decode_output_button.config(state=tk.DISABLED)

    def browse_encode_input(self) -> None:
        """Browse for encode input file"""
        filename = filedialog.askopenfilename(
            title="Select input file",
            filetypes=[
                ("All supported files", "*.png *.jpg *.jpeg *.wav *.txt *.md"),
                ("Image files", "*.png *.jpg *.jpeg"),
                ("Audio files", "*.wav"),
                ("Text files", "*.txt *.md"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.encode_input_path.set(filename)

    def browse_encode_output(self) -> None:
        """Browse for encode output file"""
        filename = filedialog.asksaveasfilename(
            title="Select output file",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("WAV files", "*.wav"),
                ("Text files", "*.txt *.md"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.encode_output_path.set(filename)

    def browse_encode_message_file(self) -> None:
        """Browse for message file to encode"""
        filename = filedialog.askopenfilename(
            title="Select message file", filetypes=[("All files", "*.*")]
        )
        if filename:
            self.encode_message_file.set(filename)

    def browse_decode_input(self) -> None:
        """Browse for decode input file"""
        filename = filedialog.askopenfilename(
            title="Select input file",
            filetypes=[
                ("All supported files", "*.png *.jpg *.jpeg *.wav *.txt *.md"),
                ("Image files", "*.png *.jpg *.jpeg"),
                ("Audio files", "*.wav"),
                ("Text files", "*.txt *.md"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.decode_input_path.set(filename)

    def browse_decode_output(self) -> None:
        """Browse for decode output file"""
        filename = filedialog.asksaveasfilename(
            title="Select output file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if filename:
            self.decode_output_path.set(filename)

    def browse_capacity_input(self) -> None:
        """Browse for capacity check input file"""
        filename = filedialog.askopenfilename(
            title="Select input file",
            filetypes=[
                ("All supported files", "*.png *.jpg *.jpeg *.wav *.txt *.md"),
                ("Image files", "*.png *.jpg *.jpeg"),
                ("Audio files", "*.wav"),
                ("Text files", "*.txt *.md"),
                ("All files", "*.*"),
            ],
        )
        if filename:
            self.capacity_input_path.set(filename)

    def detect_file_type(self, filepath: str) -> str:
        """Detect file type based on extension

        Args:
            filepath: Path to the file

        Returns:
            File type: 'image', 'audio', 'text', or 'unknown'
        """
        ext = get_file_extension(filepath)

        if ext in [".png", ".jpg", ".jpeg"]:
            return "image"
        if ext in [".wav"]:
            return "audio"
        if ext in [".txt", ".md"]:
            return "text"
        return "unknown"

    def encode_message(self) -> None:  # pylint: disable=too-many-return-statements,too-many-branches
        """Encode message into file"""
        # Validate inputs
        input_path = self.encode_input_path.get()
        output_path = self.encode_output_path.get()

        if not input_path:
            messagebox.showerror("Error", "Please select an input file")
            return

        if not output_path:
            messagebox.showerror("Error", "Please select an output file")
            return

        if not Path(input_path).exists():
            messagebox.showerror("Error", f"Input file does not exist: {input_path}")
            return

        # Get message
        message: Optional[str] = None
        file_path: Optional[str] = None

        if self.encode_message_source.get() == "text":
            message = self.encode_message_text.get("1.0", tk.END).strip()
            if not message:
                messagebox.showerror("Error", "Please enter a message to encode")
                return
        else:
            file_path = self.encode_message_file.get()
            if not file_path:
                messagebox.showerror("Error", "Please select a message file")
                return
            if not Path(file_path).exists():
                messagebox.showerror(
                    "Error", f"Message file does not exist: {file_path}"
                )
                return

        # Detect file type
        file_type = self.detect_file_type(input_path)

        if file_type == "unknown":
            messagebox.showerror(
                "Error",
                f"Unsupported file format: {get_file_extension(input_path)}\n"
                "Supported formats: PNG, JPEG (images), WAV (audio), TXT, MD (text)",
            )
            return

        # Encode based on file type
        try:
            success = False

            if file_type == "image":
                success = encode_image(input_path, output_path, message, file_path)
            elif file_type == "audio":
                success = encode_audio(input_path, output_path, message, file_path)
            elif file_type == "text":
                method = self.encode_text_method.get()
                success = encode_text(
                    input_path, output_path, message, file_path, method
                )

            if success:
                messagebox.showinfo(
                    "Success",
                    f"Message successfully encoded into {output_path}",
                )
            else:
                messagebox.showerror(
                    "Error", "Encoding failed. Check console for details."
                )

        except (OSError, ValueError, UnicodeError, AttributeError, TypeError) as e:
            messagebox.showerror("Error", f"Encoding failed: {str(e)}")

    def decode_message(self) -> None:  # pylint: disable=too-many-branches
        """Decode message from file"""
        # Validate inputs
        input_path = self.decode_input_path.get()

        if not input_path:
            messagebox.showerror("Error", "Please select an input file")
            return

        if not Path(input_path).exists():
            messagebox.showerror("Error", f"Input file does not exist: {input_path}")
            return

        # Detect file type
        file_type = self.detect_file_type(input_path)

        if file_type == "unknown":
            messagebox.showerror(
                "Error",
                f"Unsupported file format: {get_file_extension(input_path)}\n"
                "Supported formats: PNG, JPEG (images), WAV (audio), TXT, MD (text)",
            )
            return

        # Decode based on file type
        try:
            decoded_message: Optional[str] = None

            if file_type == "image":
                decoded_message = decode_image(input_path)
            elif file_type == "audio":
                decoded_message = decode_audio(input_path)
            elif file_type == "text":
                method = self.decode_text_method.get()
                decoded_message = decode_text(input_path, method)

            if decoded_message:
                # Display in text widget
                self.decode_result_text.delete("1.0", tk.END)
                self.decode_result_text.insert("1.0", decoded_message)

                # Save to file if requested
                if self.decode_save_to_file.get():
                    output_path = self.decode_output_path.get()
                    if output_path:
                        try:
                            Path(output_path).write_text(
                                decoded_message, encoding="utf-8"
                            )
                            messagebox.showinfo(
                                "Success",
                                f"Message decoded successfully!\n"
                                f"Saved to: {output_path}",
                            )
                        except (OSError, IOError, UnicodeError) as e:
                            messagebox.showwarning(
                                "Partial Success",
                                f"Message decoded but failed to save to "
                                f"file:\n{str(e)}",
                            )
                    else:
                        messagebox.showinfo(
                            "Success",
                            "Message decoded successfully!\n"
                            "Please specify output file to save.",
                        )
                else:
                    messagebox.showinfo("Success", "Message decoded successfully!")
            else:
                messagebox.showerror(
                    "Error", "Decoding failed. Check console for details."
                )

        except (OSError, ValueError, UnicodeError, AttributeError, TypeError) as e:
            messagebox.showerror("Error", f"Decoding failed: {str(e)}")

    def check_capacity(self) -> None:
        """Check capacity of media file"""
        # Validate inputs
        input_path = self.capacity_input_path.get()

        if not input_path:
            messagebox.showerror("Error", "Please select an input file")
            return

        if not Path(input_path).exists():
            messagebox.showerror(
                "Error", f"Input file does not exist: {input_path}"
            )
            return

        # Detect file type
        file_type = self.detect_file_type(input_path)

        if file_type == "unknown":
            messagebox.showerror(
                "Error",
                f"Unsupported file format: {get_file_extension(input_path)}\n"
                "Supported formats: PNG, JPEG (images), WAV (audio), TXT, MD (text)",
            )
            return

        # Check capacity based on file type
        try:
            result = ""

            if file_type == "image":
                capacity = get_image_capacity(input_path)
                result = (
                    f"File: {Path(input_path).name}\n"
                    f"Type: Image\n"
                    f"Capacity: {capacity} characters\n\n"
                    f"This image can hide approximately:\n"
                    f"  - {capacity} characters of text\n"
                    f"  - {capacity // 1024} KB of data"
                )
            elif file_type == "audio":
                capacity = get_audio_capacity(input_path)
                result = (
                    f"File: {Path(input_path).name}\n"
                    f"Type: Audio (WAV)\n"
                    f"Capacity: {capacity} characters\n\n"
                    f"This audio file can hide approximately:\n"
                    f"  - {capacity} characters of text\n"
                    f"  - {capacity // 1024} KB of data"
                )
            elif file_type == "text":
                result = (
                    f"File: {Path(input_path).name}\n"
                    f"Type: Text\n\n"
                    f"Text steganography capacity depends on the cover text length.\n"
                    f"For whitespace encoding: ~1 bit per space character\n"
                    f"For zero-width encoding: ~2 bits per character\n\n"
                    f"Use the encode function to test if your message fits."
                )

            # Display result
            self.capacity_result_text.delete("1.0", tk.END)
            self.capacity_result_text.insert("1.0", result)

        except (OSError, ValueError, AttributeError, TypeError) as e:
            messagebox.showerror("Error", f"Capacity check failed: {str(e)}")


def main() -> None:
    """Main entry point for GUI"""
    root = tk.Tk()
    SteganoGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
