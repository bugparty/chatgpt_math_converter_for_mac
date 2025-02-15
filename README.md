# ChatGPT Math Notation Converter for Mac

A lightweight macOS utility that automatically converts ChatGPT's LaTeX-style math notation to standard Markdown math syntax in your clipboard.

## Features

- Runs silently in the background monitoring your clipboard
- Automatically converts math notation when you copy text from ChatGPT
- Converts `\[...\]` to `$$...$$` for block equations
- Converts `\(...\)` to `$...$` for inline equations
- Zero configuration needed

## Prerequisites

- macOS
- Python 3.x
- pyobjc package

## Installation

1. Install the required dependency:
    ```sh
    pip install pyobjc
    ```

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/gptcliphelper.git
    cd gptcliphelper
    ```

2. Run the script:
    ```sh
    python macclip.py
    ```

3. The utility will start running in the background, monitoring your clipboard for any copied text from ChatGPT and converting the math notation automatically.

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
