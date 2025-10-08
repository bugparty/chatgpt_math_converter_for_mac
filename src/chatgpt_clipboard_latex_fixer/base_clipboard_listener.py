from abc import ABC, abstractmethod
from .common import convert_math_syntax


class BaseClipboardListener(ABC):
    """Base class for clipboard listeners across different platforms"""
    
    def __init__(self):
        """Initialize the base clipboard listener"""
        self.last_processed_content = None  # Save the last processed content to avoid redundant processing
    
    @abstractmethod
    def get_clipboard_text(self):
        """
        Get text content from clipboard.
        Must be implemented by subclasses.
        
        Returns:
            str: The clipboard text content, or None if unavailable
        """
        pass
    
    @abstractmethod
    def set_clipboard_text(self, text):
        """
        Set text content to clipboard.
        Must be implemented by subclasses.
        
        Args:
            text (str): The text to set in the clipboard
        """
        pass
    
    @abstractmethod
    def start(self):
        """
        Start listening to clipboard changes.
        Must be implemented by subclasses.
        """
        pass
    
    def on_clipboard_change(self, content):
        """
        Process the changed clipboard content.
        This method can be overridden by subclasses if needed.
        
        Args:
            content (str): The clipboard content to process
        """
        # Use convert_math_syntax to transform the content
        converted_content = convert_math_syntax(content)

        # If the converted content is the same as the current content, skip writing back to avoid loops
        if converted_content == content:
            print("Converted content is the same as the original content, skipping write-back")
            self.last_processed_content = content
            return

        print(f"Original clipboard content: {content}...")  # Show first 300 chars
        print(f"Converted clipboard content: {converted_content}...")  # Show first 300 chars

        # Save the processed content
        self.last_processed_content = converted_content

        # Write the converted content back to the clipboard
        self.set_clipboard_text(converted_content)
