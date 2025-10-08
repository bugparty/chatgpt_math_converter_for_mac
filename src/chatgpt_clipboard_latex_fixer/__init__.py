"""ChatGPT Clipboard LaTeX Fixer - Convert LaTeX-style math notation to Markdown format."""

__version__ = "0.1.0"

from .common import convert_math_syntax
from .clipboard_factory import create_clipboard_listener

__all__ = [
    "convert_math_syntax",
    "create_clipboard_listener",
]
