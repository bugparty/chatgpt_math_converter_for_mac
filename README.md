# ChatGPT Clipboard LaTeX Fixer

A lightweight cross-platform utility that automatically converts ChatGPT's LaTeX-style math notation to standard Markdown math syntax in your clipboard.

## Features

- **Cross-platform support**: Works on both Windows and macOS
- Runs silently in the background monitoring your clipboard
- Automatically converts math notation when you copy text from ChatGPT
- Converts `\[...\]` to `$$...$$` for block equations
- Converts `\(...\)` to `$...$` for inline equations
- Converts `[...]` to `$$...$$` for block equations
- Removes extra spaces in inline math: `$ xxx $` → `$xxx$`
- Zero configuration needed - automatically detects your platform

## Installation

### From PyPI (Recommended)

```bash
pip install chatgpt-clipboard-latex-fixer
```

**Platform-specific dependencies:**

**Windows:**
```bash
pip install chatgpt-clipboard-latex-fixer pywin32
```

**macOS:**
```bash
pip install chatgpt-clipboard-latex-fixer pyobjc
```

### From Source

1. Clone the repository:
    ```sh
    git clone https://github.com/bugparty/chatgpt_math_converter_for_mac.git
    cd chatgpt_math_converter_for_mac
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Command Line (After pip install)

Simply run:
```sh
chatgpt-clipboard-latex-fixer
```

The utility will start running in the background, monitoring your clipboard for any copied text from ChatGPT and converting the math notation automatically.

Press `Ctrl+C` to stop the listener.

### From Source

1. Clone the repository:
    ```sh
    git clone https://github.com/bugparty/chatgpt_math_converter_for_mac.git
    cd chatgpt_math_converter_for_mac
    ```

2. Run the main script (works on both platforms):
    ```sh
    python main.py
    ```
    
    Or run the platform-specific script directly:
    
    **macOS:**
    ```sh
    python macclip.py
    ```
    
    **Windows:**
    ```sh
    python winclip.py
    ```

3. The utility will start running in the background, monitoring your clipboard for any copied text from ChatGPT and converting the math notation automatically.

4. Press `Ctrl+C` to stop the listener.

## Project Structure

- `main.py` - Cross-platform entry point (recommended)
- `clipboard_factory.py` - Factory pattern for creating platform-specific listeners
- `common.py` - Shared math conversion logic
- `macclip.py` - macOS-specific clipboard listener implementation
- `winclip.py` - Windows-specific clipboard listener implementation

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
