# pip install pyobjc
from AppKit import NSPasteboard, NSApplication, NSPasteboardTypeString
from Foundation import NSObject, NSLog
import objc
import time
import re

# conver chatgpt math syntax to common markdown
def convert_math_syntax(input_text):
    # turn  \[...\] into $$...$$ format
    output_text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', input_text, flags=re.DOTALL)
    # turn  \(...\) into $...$ format
    output_text = re.sub(r'\\\((.*?)\\\)', r'$\1$', output_text, flags=re.DOTALL)
    # turn $ xxx $ into $xxx$ format
    output_text = re.sub(r'\$\s*(.*?)\s*\$', r'$\1$', output_text, flags=re.DOTALL)
    
    return output_text


class ClipboardListener(NSObject):
    def init(self):
        """Override the init method and initialize using objc.super"""
        self = objc.super(ClipboardListener, self).init()
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
        NSLog(f"Original clipboard content: {content}")

        # Use convert_math_syntax to transform the content
        converted_content = convert_math_syntax(content)

        # If the converted content is the same as the current content, skip writing back to avoid loops
        if converted_content == content:
            NSLog("Converted content is the same as the original content, skipping write-back")
            return

        NSLog(f"Converted clipboard content: {converted_content}")

        # Save the processed content
        self.last_processed_content = converted_content

        # Write the converted content back to the clipboard
        self.pasteboard.declareTypes_owner_([NSPasteboardTypeString], None)
        self.pasteboard.setString_forType_(converted_content, NSPasteboardTypeString)


def main():
    listener = ClipboardListener.alloc().init()   # Create an instance using alloc().init()
    if listener is None:
        print("Failed to initialize clipboard listener")
        return

    print("Listening for clipboard content changes...")
    try:
        while True:
            listener.check_clipboard()  # Check for clipboard content changes
            time.sleep(0.5)  # Check every 0.5 seconds
    except KeyboardInterrupt:
        print("Stopped listening")
        NSApplication.sharedApplication().terminate_(None)


if __name__ == "__main__":
    main()