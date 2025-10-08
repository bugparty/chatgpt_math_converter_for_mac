# pip install pyobjc
from AppKit import NSPasteboard, NSApplication, NSPasteboardTypeString
from Foundation import NSObject, NSLog
import objc
import time
from .common import convert_math_syntax


class MacClipboardListener(NSObject):
    """
    macOS clipboard listener implementation.
    Note: Must inherit from NSObject for Objective-C compatibility,
    so we implement the base listener interface rather than inherit from it.
    """
    def init(self):
        """Override the init method and initialize using objc.super"""
        self = objc.super(MacClipboardListener, self).init()
        if self is None:
            return None

        try:
            # Initialize the clipboard object and related properties
            self.pasteboard = NSPasteboard.generalPasteboard()
            self.last_change_count = self.pasteboard.changeCount()  # Initial change count
            self.last_processed_content = None   # Save the last processed content to avoid redundant processing
            NSLog("Clipboard listener successfully initialized")
        except Exception as e:
            NSLog(f"Failed to initialize clipboard: {e}")
            self.pasteboard = None

        return self

    def check_clipboard(self):
        """Check if clipboard content has changed"""
        if not self.pasteboard:
            NSLog("Error: Clipboard is not initialized")
            return

        try:
            # Get the current change count of the clipboard
            current_change_count = self.pasteboard.changeCount()
            if current_change_count != self.last_change_count:
                self.last_change_count = current_change_count

                # Get the content of the clipboard
                content = self.pasteboard.stringForType_("public.utf8-plain-text")
                if content and content != self.last_processed_content:  # Skip redundant processing
                    self.on_clipboard_change(content)
        except Exception as e:
            NSLog(f"Error while checking clipboard: {e}")

    def on_clipboard_change(self, content):
        """Process the changed clipboard content"""
        # Use convert_math_syntax to transform the content
        converted_content = convert_math_syntax(content)

        # If the converted content is the same as the current content, skip writing back to avoid loops
        if converted_content == content:
            NSLog("Converted content is the same as the original content, skipping write-back")
            self.last_processed_content = content
            return

        NSLog(f"Original clipboard content: {content[:100]}...")
        NSLog(f"Converted clipboard content: {converted_content[:100]}...")

        # Save the processed content
        self.last_processed_content = converted_content

        # Write the converted content back to the clipboard (set_clipboard_text equivalent)
        self.pasteboard.declareTypes_owner_([NSPasteboardTypeString], None)
        self.pasteboard.setString_forType_(converted_content, NSPasteboardTypeString)
    
    def get_clipboard_text(self):
        """Get text content from clipboard"""
        if not self.pasteboard:
            return None
        try:
            return self.pasteboard.stringForType_("public.utf8-plain-text")
        except Exception as e:
            NSLog(f"Error getting clipboard content: {e}")
            return None
    
    def set_clipboard_text(self, text):
        """Set text content to clipboard"""
        try:
            self.pasteboard.declareTypes_owner_([NSPasteboardTypeString], None)
            self.pasteboard.setString_forType_(text, NSPasteboardTypeString)
        except Exception as e:
            NSLog(f"Error setting clipboard content: {e}")

    def start(self):
        """Start listening to clipboard changes"""
        print("Listening for clipboard content changes...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.check_clipboard()  # Check for clipboard content changes
                time.sleep(0.5)  # Check every 0.5 seconds
        except KeyboardInterrupt:
            print("\nStopped listening")
            NSApplication.sharedApplication().terminate_(None)


def main():
    listener = MacClipboardListener.alloc().init()   # Create an instance using alloc().init()
    if listener is None:
        print("Failed to initialize clipboard listener")
        return

    listener.start()


if __name__ == "__main__":
    main()